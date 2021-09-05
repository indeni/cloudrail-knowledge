import dataclasses
import json
import os
import shutil
import tempfile
import unittest
import uuid
from abc import abstractmethod

from cloudrail.knowledge.context.cloud_provider import CloudProvider

from cloudrail.cli.api_client.external_api_client import ExternalApiClient
from cloudrail.cli.terraform_service.terraform_context_service import TerraformContextService
from cloudrail.cli.terraform_service.terraform_plan_converter import TerraformPlanConverter
from common.api.dtos.cloud_provider_dto import CloudProviderDTO
from common.constants import IacType
from common.ip_encryption_utils import EncryptionMode, encode_ips_in_file
from common.utils.customer_string_utils import CustomerStringUtils
from common.utils.file_utils import write_to_file
from core.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from core.environment_context.terraform_resource_finder import TerraformResourceFinder
from core.services.drift_detection.environment_context_drift_detector_factory import EnvironmentContextDriftDetectorFactory
from test.knowledge.context.aws_context_test import AwsContextTest


class BaseDriftTest(unittest.TestCase):
    DUMMY_CUSTOMER_ID: str = '00000000-0000-0000-0000-000000000000'
    REGION: str = 'us-east-1'

    @abstractmethod
    def get_component(self):
        pass

    @staticmethod
    def get_provider_name():
        return 'aws'

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.scenarios_dir = os.path.join(os.path.abspath(os.path.join(self.current_dir, '')), f'{self.get_provider_name()}/scenarios')
        self.test_files = []
        CustomerStringUtils.set_hashcode_salt(self.DUMMY_CUSTOMER_ID)

    def run_test_case(self, module_path: str, assert_func):
        TerraformResourceFinder.initialize()
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        module_path = '{}/{}'.format(self.get_component(), module_path)
        scenario_folder = os.path.join(self.scenarios_dir, module_path)
        shutil.copytree(scenario_folder, working_dir)
        cached_plan_for_drift_path = os.path.join(working_dir, 'cached_plan_for_drift.json')
        account_data_for_drift_path = os.path.join(working_dir, 'account-data-for-drift')
        iac_url_template = 'https://{iac_file_path}#{iac_file_line_no}'
        try:
            if not os.path.isfile(cached_plan_for_drift_path):
                raise Exception(f'missing cached_plan_for_drift.json for {scenario_folder}')
            shutil.unpack_archive(account_data_for_drift_path + '.zip', extract_dir=account_data_for_drift_path, format='zip')
            environment_context_builder = EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES, IacType.TERRAFORM)
            scanner_context = environment_context_builder.build(account_data_for_drift_path, None,
                                                                ignore_exceptions=True, run_enrichment_requiring_aws=False)
            account_id = next(iter(scanner_context.accounts)).account
            context_service = TerraformContextService(TerraformPlanConverter())
            terraform_result = context_service.process_json_result(cached_plan_for_drift_path,
                                                                   AwsContextTest.get_supported_services(self),
                                                                   {},
                                                                   self.DUMMY_CUSTOMER_ID,
                                                                   ExternalApiClient.get_cli_handshake_version(),
                                                                   '',
                                                                   CloudProviderDTO.AMAZON_WEB_SERVICES)
            output_path = os.path.join(cached_plan_for_drift_path.replace('cached_plan_for_drift.json', 'output.json'))
            write_to_file(output_path, terraform_result.result)
            encode_ips_in_file(output_path, self.DUMMY_CUSTOMER_ID, EncryptionMode.DECRYPT)
            iac_context_before = environment_context_builder.build(None,
                                                                   output_path,
                                                                   account_id,
                                                                   ignore_exceptions=True, run_enrichment_requiring_aws=False,
                                                                   use_after_data=False, iac_url_template=iac_url_template)
            iac_context_after = environment_context_builder.build(None,
                                                                  output_path,
                                                                  account_id,
                                                                  ignore_exceptions=True, run_enrichment_requiring_aws=False,
                                                                  use_after_data=True, keep_deleted_entities=False,
                                                                  iac_url_template=iac_url_template)
            result = EnvironmentContextDriftDetectorFactory.get(CloudProvider.AMAZON_WEB_SERVICES).find_drifts(scanner_context, iac_context_before,
                                                                                                              iac_context_after, 'workspace')
            json.dumps([dataclasses.asdict(r) for r in result.drifts])
            assert_func(self, result.drifts)
        finally:
            TerraformResourceFinder.destroy()
            shutil.rmtree(working_dir, ignore_errors=True)


def drift_test(module_path: str):
    def test_case_decorator(test_case_function):
        def test_case_executor(test_class_instance):
            test_class_instance.run_test_case(module_path, test_case_function)

        return test_case_executor

    return test_case_decorator
