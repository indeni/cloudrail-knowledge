import inspect
import json
import os
import shutil
import unittest
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Callable
from cloudrail.knowledge.rules.rule_metadata import RuleMetadata
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.rules.rules_metadata_store import CloudrailRulesMetadataStore
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer
from cloudrail.knowledge.rules.base_rule import RuleResponse, RuleResultType
from cloudrail.knowledge.rules.rules_executor import RulesExecutor
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore
from cloudrail.knowledge.utils.utils import get_account_id


def rule_test(*args, **kwargs) -> Callable:
    def _rules_tests_wrapper(test_case_func: Callable) -> Callable:
        def test_case_wrapper(self) -> None:
            self._run_test_case(test_case_func, *args, **kwargs)
        return test_case_wrapper
    return _rules_tests_wrapper


class BaseRuleTest(unittest.TestCase):

    DUMMY_CUSTOMER_ID: str = '00000000-0000-0000-0000-000000000000'
    RULES_METADATA: CloudrailRulesMetadataStore = CloudrailRulesMetadataStore()

    def __init__(self, *args, **kwargs):
        # pylint: disable=super-with-arguments
        super(BaseRuleTest, self).__init__(*args, **kwargs)
        self.account_id = None
        self.account_data = None
        self.output_path = None
        self.salt = None
        self.tenant_id = str(uuid.uuid4())

    @abstractmethod
    def get_rule(self):
        pass

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.test_files = []
        self.rule_under_test = self.get_rule()
        if not os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION')):
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    def _get_full_path(self, dir_path: str) -> str:
        abs_path = os.path.abspath(dir_path)
        if os.path.isdir(abs_path):
            return abs_path
        dir_path = os.path.join(Path(inspect.getfile(self.__class__)).parent.absolute(), dir_path)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            raise Exception('cannot find dir path {}'.format(dir_path))

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(json.dumps(result))
        return dest_path

    def _run_test_case(self, test_function: Callable,
                       test_case_folder: str,
                       should_alert: bool = True,
                       number_of_issue_items: int = 1) -> None:
        self._run_terraform_test_case(test_function, test_case_folder, should_alert, number_of_issue_items)
        self._run_cloudformation_test_case(test_function, test_case_folder, should_alert, number_of_issue_items)

    def _run_terraform_test_case(self, test_function: Callable,
                                 test_case_folder: str,
                                 should_alert: bool = True,
                                 number_of_issue_items: int = 1) -> None:
        print(f'about to execute Terraform \'{test_function.__name__}\' scenario')
        local_account_data = None
        try:
            # Arrange
            TerraformResourceFinder.initialize()
            test_case_folder_full_path = self._get_full_path(test_case_folder)
            local_account_data = os.path.join(test_case_folder_full_path, 'account-data')
            account_data_zip = f'{local_account_data}.zip'

            if os.path.isfile(account_data_zip):
                shutil.unpack_archive(account_data_zip, extract_dir=local_account_data, format='zip')
                self.account_data = local_account_data
            elif self.get_default_account_data_path():
                shutil.unpack_archive(self.get_default_account_data_path(), extract_dir=local_account_data, format='zip')
                self.account_data = local_account_data
            else:
                self.account_data = None

            self.account_id = self.get_account_id(self.account_data)
            self.salt = self.DUMMY_CUSTOMER_ID
            plan_json = os.path.join(test_case_folder_full_path, 'cached_plan.json')
            self._validate_supported_iac_type(IacType.TERRAFORM, plan_json)
            result = TerraformShowOutputTransformer.transform(plan_json,
                                                                    '',
                                                                    self.get_supported_service(),
                                                                    self.salt)
            self.output_path = self._save_result_to_file(result,
                                                         os.path.join(test_case_folder_full_path, 'output.json'))
            self.test_files.append(self.output_path)
            context = self.build_environment_context()
            self._execute_rule_and_assert(iac_type=IacType.TERRAFORM,
                                          env_context=context,
                                          should_alert=should_alert,
                                          number_of_issue_items=number_of_issue_items,
                                          test_function=test_function)
        finally:
            TerraformResourceFinder.destroy()
            if self.account_data and Path(self.account_data).parent.name == Path(local_account_data).parent.name:
                shutil.rmtree(local_account_data, ignore_errors=True)

    def _run_cloudformation_test_case(self, test_function: Callable,
                                      test_case_folder: str,
                                      should_alert: bool = True,
                                      number_of_issue_items: int = 1) -> None:
        test_case_folder_full_path = self._get_full_path(test_case_folder)
        cfn_template_yaml_file: str = os.path.join(test_case_folder_full_path, 'cloudformation.yaml')
        if os.path.exists(cfn_template_yaml_file):
            print(f'about to execute CloudFormation \'{test_function.__name__}\' scenario')
            try:
                local_account_data_zip = os.path.join(test_case_folder_full_path, 'cfn-account-data.zip')
                self._validate_supported_iac_type(IacType.CLOUDFORMATION, cfn_template_yaml_file)
                local_account_data = os.path.join(test_case_folder_full_path, 'cfn-account-data')
                if os.path.isfile(local_account_data_zip):
                    shutil.unpack_archive(local_account_data_zip, extract_dir=local_account_data, format='zip')
                    self.account_data = local_account_data
                else:
                    shutil.unpack_archive(self.get_default_account_data_path('default-cfn-account-data.zip'), extract_dir=local_account_data, format='zip')
                    self.account_data = local_account_data

                self.account_id = self.get_account_id(self.account_data)
                self.customer_id = self.DUMMY_CUSTOMER_ID

                context = EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                            IacType.CLOUDFORMATION) \
                    .build(account_data_dir_path=self.account_data,
                        iac_file_path=cfn_template_yaml_file, account_id=self.account_id,
                        salt=self.customer_id, **{'region': 'us-east-1', 'stack_name': 'testCfnStack'})

                self._execute_rule_and_assert(iac_type=IacType.CLOUDFORMATION, env_context=context,
                                            should_alert=should_alert,
                                            number_of_issue_items=number_of_issue_items,
                                            test_function=test_function)
            finally:
                if self.account_data and Path(self.account_data).parent.name == Path(local_account_data).parent.name:
                    shutil.rmtree(local_account_data, ignore_errors=True)

    def _validate_supported_iac_type(self, iac_type: IacType, iac_file_path: str) -> None:
        metadata: RuleMetadata = self.RULES_METADATA.get_by_rule_id(self.get_rule().get_id())
        supported: bool = iac_type in metadata.supported_iac_types
        if supported and not os.path.exists(iac_file_path):
            raise AssertionError(f'rule={self.get_rule().get_id()} missing IaC file')
        elif not supported and os.path.exists(iac_file_path):
            raise AssertionError(f'rule={self.get_rule().get_id()} is disabled for IaC={iac_type.value}')

    @abstractmethod
    def build_environment_context(self):
        pass

    @abstractmethod
    def get_default_account_data_path(self, file_name: str = None):
        pass

    @abstractmethod
    def get_account_id(self, account_data):
        pass

    @abstractmethod
    def get_supported_service(self):
        pass

    @abstractmethod
    def get_cloud_provider(self):
        pass

    def _execute_rule_and_assert(self, iac_type: IacType, env_context: BaseEnvironmentContext, should_alert: bool,
                                 number_of_issue_items: int,
                                 test_function: Callable,) -> None:
        rule_start_time: datetime = datetime.now()
        rule_result: RuleResponse = RulesExecutor.execute(self.get_cloud_provider(), env_context, [self.rule_under_test.get_id()])[0]
        rule_result.iac_type = iac_type
        self._assert_rule(rule_result=rule_result, should_alert=should_alert,
                          number_of_issue_items=number_of_issue_items, rule_start_time=rule_start_time,
                          test_function=test_function)

    def _assert_rule(self, rule_result: RuleResponse, should_alert: bool,
                     number_of_issue_items: int, rule_start_time: datetime,
                     test_function: Callable) -> None:
        rule_end_time = datetime.now()
        rule_runtime_seconds = (rule_end_time - rule_start_time).total_seconds()
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, rule_result.status)
            self.assertEqual(number_of_issue_items, len(rule_result.issues), rule_result.issues)
            for issue in rule_result.issues:
                self._assert_evidence(issue.evidence)
        else:
            self.assertNotEqual(RuleResultType.FAILED, rule_result.status,
                                f'rule result failed and it shouldn\'t have: {rule_result.issues}')

        self.assertLess(rule_runtime_seconds, 20,
                        f'The test {self.rule_under_test.get_id()} took {rule_runtime_seconds} seconds to run')
        test_function(self, rule_result)

    def _assert_evidence(self, evidence_str: str):
        self.assertRegex(evidence_str, r'^[A-Za-z0-9-_#?:\'".,\s`~/\\()\[\]*{}\$]+$', '')


class AzureBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.AZURE

    def get_account_id(self, account_data):
        return 'ae7905ce-4577-4a32-934b-9f662c77869d'

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE, IacType.TERRAFORM).build(self.account_data,
                                                                                                  self.output_path,
                                                                                                  self.account_id,
                                                                                                  tenant_id=self.tenant_id)

    def get_default_account_data_path(self, file_name: str = None):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', file_name or 'account-data-default-azure.zip')

    def get_supported_service(self):
        return IacFieldsStore.get_azure_supported_services()


class AwsBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.AMAZON_WEB_SERVICES

    def get_supported_service(self):
        return IacFieldsStore.get_terraform_aws_supported_services()

    def get_account_id(self, account_data):
        return get_account_id(account_data)

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(self.account_data,
                                                                             self.output_path,
                                                                             self.account_id,
                                                                             self.salt)

    def get_default_account_data_path(self, file_name: str = None):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', file_name or 'account-data-vpc-platform.zip')


class GcpBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.GCP

    def get_account_id(self, account_data):
        return 'dev-tomer'  # TODO: create a project for tests and put project-id here

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(self.account_data,
                                                                                                self.output_path,
                                                                                                self.account_id)

    def get_default_account_data_path(self, file_name: str = None):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', file_name or 'account-data-gcp-default-vpc-network.zip')

    def get_supported_service(self):
        return IacFieldsStore.get_terraform_gcp_supported_services()
