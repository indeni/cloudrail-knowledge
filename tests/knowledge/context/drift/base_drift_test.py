import dataclasses
import json
import os
import shutil
import tempfile
import unittest
import uuid
from abc import ABC, abstractmethod

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.drift_detection.environment_context_drift_detector_factory import EnvironmentContextDriftDetectorFactory
from cloudrail.knowledge.utils.file_utils import write_to_file
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer
from cloudrail.knowledge.utils.utils import get_account_id, get_project_id


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
    def get_account_id_from_account_data(self, account_data: str, from_live_env: bool = False):
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
            customer_id = self.DUMMY_SALT
            if not from_live_env:
                result = TerraformShowOutputTransformer.transform(cached_plan_for_drift_path,
                                                                  '',
                                                                  self.get_supported_services(),
                                                                  self.DUMMY_SALT)
                output_path = os.path.join(cached_plan_for_drift_path.replace('cached_plan_for_drift.json', 'output.json'))
                write_to_file(output_path, json.dumps(result))
            else:
                customer_id = live_customer_id
                output_path = cached_plan_for_drift_path
            drift_detector = EnvironmentContextDriftDetectorFactory.get(self.get_provider())
            result = drift_detector.find_drifts(provider=self.get_provider(),
                                                iac_type=IacType.TERRAFORM,
                                                account_data=account_data_for_drift_path,
                                                iac_file_before=output_path,
                                                iac_file_after=output_path,
                                                salt=customer_id,
                                                account_id=self.get_account_id_from_account_data(account_data_for_drift_path, from_live_env),
                                                iac_url_template=iac_url_template,
                                                workspace_id='workspace')
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

    def get_account_id_from_account_data(self, account_data: str, from_live_env: bool = False):
        if from_live_env:
            return get_account_id(account_data)
        return '000000000000'


class BaseAzureDriftTest(BaseDriftTest, ABC):

    def get_provider(self) -> CloudProvider:
        return CloudProvider.AZURE

    def get_supported_services(self):
        return IacFieldsStore.get_azure_supported_services()

    def get_account_id_from_account_data(self, account_data: str, from_live_env: bool = False):
        return None


class BaseGcpDriftTest(BaseDriftTest, ABC):

    def get_provider(self) -> CloudProvider:
        return CloudProvider.GCP

    def get_supported_services(self):
        return IacFieldsStore.get_terraform_gcp_supported_services()

    def get_account_id_from_account_data(self, account_data: str, from_live_env: bool = False):
        return get_project_id(account_data)

