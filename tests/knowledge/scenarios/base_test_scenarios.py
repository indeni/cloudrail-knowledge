import json
import os
import shutil
import unittest
from typing import List

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.rules.aws_rules_loader import AwsRulesLoader
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.rules_executor import RulesExecutor
from cloudrail.knowledge.utils.utils import get_account_id
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer


class BaseTestScenarios(unittest.TestCase):

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.test_files = []
        self.rules_under_test = AwsRulesLoader().load().keys()
        self.account_id = None
        self.account_data = None
        self.output_path = None
        self.salt = None

    @staticmethod
    def _get_full_path(dir_path: str) -> str:
        abs_path = os.path.abspath(dir_path)
        if os.path.isdir(abs_path):
            return abs_path
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_path)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            raise Exception('cannot find dir path {}'.format(dir_path))

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(json.dumps(result))
        return dest_path

    def run_test_case(self, test_case_folder: str,
                      failed_rule_ids: List[str] = None):

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
            self.salt = '00000000-0000-0000-0000-000000000000'
            plan_json = os.path.join(test_case_folder_full_path, 'cached_plan.json')
            result = TerraformShowOutputTransformer.transform(plan_json,
                                                              '',
                                                              self.get_supported_service(),
                                                              self.salt)
            self.output_path = self._save_result_to_file(result,
                                                         os.path.join(test_case_folder_full_path, 'output.json'))
            self.test_files.append(self.output_path)
            context = self.build_environment_context()

            # Act
            rules_results = RulesExecutor.execute(self.get_cloud_provider(), context, list(self.rules_under_test))
            for rule_result in rules_results:
                if failed_rule_ids and rule_result.rule_id in failed_rule_ids:
                    self.assertEqual(RuleResultType.FAILED, rule_result.status)
                    failed_rule_ids.remove(rule_result.rule_id)

            self.assertFalse(failed_rule_ids, 'not all requested rules ran: {}'.format(failed_rule_ids))
        finally:
            TerraformResourceFinder.destroy()
            if local_account_data:
                shutil.rmtree(local_account_data, ignore_errors=True)

    @staticmethod
    def set_default_account_data():
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', 'account-data-vpc-platform')

    @staticmethod
    def get_account_id(account_data):
        return get_account_id(account_data)

    @staticmethod
    def get_supported_service():
        return IacFieldsStore.get_terraform_aws_supported_services()

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(self.account_data,
                                                                             self.output_path,
                                                                             self.account_id,
                                                                             self.salt)

    @staticmethod
    def get_cloud_provider():
        return CloudProvider.AMAZON_WEB_SERVICES
