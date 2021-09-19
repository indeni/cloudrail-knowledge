import inspect
import os
import shutil
import unittest
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.rules.base_rule import RuleResponse, RuleResultType
from cloudrail.knowledge.rules.rules_executor import RulesExecutor
from cloudrail.knowledge.utils.utils import get_account_id


class BaseRuleTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        # pylint: disable=super-with-arguments
        super(BaseRuleTest, self).__init__(*args, **kwargs)
        self.account_id = None
        self.account_data = None
        self.output_path = None
        self.customer_id = None
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
        dir_path = os.path.join(self._find_caller_path(), dir_path)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            raise Exception('cannot find dir path {}'.format(dir_path))

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(result)
        return dest_path

    @staticmethod
    def _find_caller_path() -> str:
        current_file = os.path.abspath(__file__)
        stack = inspect.stack()
        for info in stack:
            # search for the first file which is not the current one.
            if os.path.abspath(info.filename) != os.path.abspath(current_file):
                return os.path.dirname(info.filename)
        return ''

    def run_test_case(self, test_case_folder: str,
                      should_alert: bool = True,
                      number_of_issue_items: int = 1) -> RuleResponse:

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
            else:
                self.account_data = self.set_default_account_data()

            self.account_id = self.get_account_id(self.account_data)
            self.customer_id = '00000000-0000-0000-0000-000000000000'
            self.output_path = os.path.join(test_case_folder_full_path, 'filtered_plan.json')
            context = self.build_environment_context()

            # Act
            rule_start_time = datetime.now()
            rule_result = RulesExecutor.execute(self.get_cloud_provider(), context, [self.rule_under_test.get_id()])[0]
            rule_end_time = datetime.now()
            rule_runtime_seconds = (rule_end_time - rule_start_time).total_seconds()
            # Assert
            if should_alert:
                self.assertEqual(RuleResultType.FAILED, rule_result.status)
                self.assertEqual(number_of_issue_items, len(rule_result.issues), rule_result.issues)
            else:
                self.assertNotEqual(RuleResultType.FAILED, rule_result.status,
                                    f'rule result failed and it shouldn\'t have: {rule_result.issues}')

            self.assertLess(rule_runtime_seconds, 20,
                            f'The test {self.rule_under_test.get_id()} took {rule_runtime_seconds} seconds to run')

            return rule_result
        finally:
            TerraformResourceFinder.destroy()
            if local_account_data:
                shutil.rmtree(local_account_data, ignore_errors=True)

    @abstractmethod
    def build_environment_context(self):
        pass

    @abstractmethod
    def set_default_account_data(self):
        pass

    @abstractmethod
    def get_account_id(self, account_data):
        pass

    @abstractmethod
    def get_cloud_provider(self):
        pass


class AzureBaseRuleTest(BaseRuleTest, ABC):
    def get_account_id(self, account_data):
        return 'ae7905ce-4577-4a32-934b-9f662c77869d'

    def get_cloud_provider(self):
        return CloudProvider.AZURE

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE, IacType.TERRAFORM).build(self.account_data,
                                                                                                  self.output_path,
                                                                                                  self.account_id,
                                                                                                  tenant_id=self.tenant_id)

    def set_default_account_data(self):
        return None


class AwsBaseRuleTest(BaseRuleTest, ABC):

    def get_account_id(self, account_data):
        return get_account_id(account_data)

    def get_cloud_provider(self):
        return CloudProvider.AMAZON_WEB_SERVICES

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(self.account_data,
                                                                             self.output_path,
                                                                             self.account_id,
                                                                             self.customer_id)

    def set_default_account_data(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', 'account-data-vpc-platform')


class GcpBaseRuleTest(BaseRuleTest, ABC):
    def get_account_id(self, account_data):
        return 'dev-tomer'  # TODO: create a project for tests and put project-id here

    def get_cloud_provider(self):
        return CloudProvider.GCP

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(self.account_data,
                                                                                                self.output_path,
                                                                                                self.account_id)

    def set_default_account_data(self):
        return None
