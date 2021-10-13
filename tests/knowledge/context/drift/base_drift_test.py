import dataclasses
import json
import os
import shutil
import tempfile
import unittest
import uuid
from abc import ABC, abstractmethod

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.drift_detection.environment_context_drift_detector_factory import EnvironmentContextDriftDetectorFactory
from cloudrail.knowledge.utils.file_utils import write_to_file
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer


class BaseDriftTest(unittest.TestCase):
    DUMMY_SALT: str = '00000000-0000-0000-0000-000000000000'
    REGION: str = 'us-east-1'

    @abstractmethod
    def get_component(self):
        pass

    @abstractmethod
    def get_supported_services(self):
        pass

    @abstractmethod
    def get_account_id_from_context(self, ctx):
        pass

    @abstractmethod
    def get_provider(self) -> CloudProvider:
        pass

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.scenarios_dir = os.path.join(os.path.abspath(os.path.join(self.current_dir, '')), f'{self.get_provider().to_shorthand_string()}')
        self.test_files = []

    def run_test_case(self, module_path: str, assert_func, from_live_env: bool, live_customer_id: str):
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
            environment_context_builder = EnvironmentContextBuilderFactory.get(self.get_provider(), IacType.TERRAFORM)
            customer_id = self.DUMMY_SALT
            if not from_live_env:
                scanner_context = environment_context_builder.build(account_data_for_drift_path,
                                                                    None,
                                                                    ignore_exceptions=True,
                                                                    run_enrichment_requiring_aws=False,
                                                                    salt=customer_id)
                result = TerraformShowOutputTransformer.transform(cached_plan_for_drift_path,
                                                                        '',
                                                                        self.get_supported_services(),
                                                                        self.DUMMY_SALT)
                output_path = os.path.join(cached_plan_for_drift_path.replace('cached_plan_for_drift.json', 'output.json'))
                write_to_file(output_path, json.dumps(result))
            else:
                customer_id = live_customer_id
                scanner_context = environment_context_builder.build(account_data_for_drift_path,
                                                                    None,
                                                                    ignore_exceptions=True,
                                                                    run_enrichment_requiring_aws=False,
                                                                    salt=customer_id)
                output_path = cached_plan_for_drift_path

            account_id = self.get_account_id_from_context(scanner_context)
            iac_context_before = environment_context_builder.build(None,
                                                                   output_path,
                                                                   account_id,
                                                                   ignore_exceptions=True, run_enrichment_requiring_aws=False,
                                                                   use_after_data=False, iac_url_template=iac_url_template,
                                                                   salt=customer_id)
            iac_context_after = environment_context_builder.build(None,
                                                                  output_path,
                                                                  account_id,
                                                                  ignore_exceptions=True, run_enrichment_requiring_aws=False,
                                                                  use_after_data=True, keep_deleted_entities=False,
                                                                  iac_url_template=iac_url_template,
                                                                  salt=customer_id)
            result = EnvironmentContextDriftDetectorFactory.get(self.get_provider()).find_drifts(scanner_context, iac_context_before,
                                                                                                 iac_context_after, 'workspace')
            json.dumps([dataclasses.asdict(r) for r in result.drifts])
            assert_func(self, result.drifts)
        finally:
            TerraformResourceFinder.destroy()
            shutil.rmtree(working_dir, ignore_errors=True)


# This test allows the possibility to test data from some live env:
# Checking the drift between cloudrail's collected cloud account-data and the TF context.
# Both can be found in the relevant S3 bucket.
# You will also need to get the customer ID, which can be found in the browsers developers tool of the drift page.
def drift_test(module_path: str, from_live_env: bool = False, live_customer_id: str = None):
    def test_case_decorator(test_case_function):
        def test_case_executor(test_class_instance):
            test_class_instance.run_test_case(module_path, test_case_function, from_live_env, live_customer_id)

        return test_case_executor

    return test_case_decorator


class BaseAwsDriftTest(BaseDriftTest, ABC):

    def get_provider(self) -> CloudProvider:
        return CloudProvider.AMAZON_WEB_SERVICES

    def get_supported_services(self):
        return IacFieldsStore.get_terraform_aws_supported_services()

    def get_account_id_from_context(self, ctx):
        return next(iter(ctx.accounts)).account


class BaseAzureDriftTest(BaseDriftTest, ABC):

    def get_provider(self) -> CloudProvider:
        return CloudProvider.AZURE

    def get_supported_services(self):
        return IacFieldsStore.get_azure_supported_services()

    def get_account_id_from_context(self, ctx):
        return None
