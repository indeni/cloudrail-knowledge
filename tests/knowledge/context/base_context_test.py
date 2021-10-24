import dataclasses
import json
import logging
import os
import shutil
import tempfile
import traceback
import unittest
import uuid
from abc import abstractmethod
from typing import Any, Dict, Optional, Type

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import CloudformationUtils
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.drift_detection.drift_detection_result import DriftDetectionResult
from cloudrail.knowledge.drift_detection.environment_context_drift_detector_factory import EnvironmentContextDriftDetectorFactory
from cloudrail.knowledge.utils import file_utils
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer

from tests.knowledge.context.test_context_annotation import TestOptions


class BaseContextTest(unittest.TestCase):
    DUMMY_ACCOUNT_ID: str = None
    DUMMY_SALT: str = '00000000-0000-0000-0000-000000000000'

    @property
    def context_builder_extra_args(self) -> Dict[str, Any]:
        return {}

    @property
    @abstractmethod
    def cloud_provider(self):
        pass

    @abstractmethod
    def get_component(self):
        pass

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    @abstractmethod
    def get_supported_services(self):
        pass

    @abstractmethod
    def get_provider_name(self):
        pass

    @abstractmethod
    def build_context(self, base_scanner_data_for_iac, output_path):
        pass

    @abstractmethod
    def get_latest_provider_block(self):
        pass

    @abstractmethod
    def get_version_provider_block(self, version):
        pass

    @abstractmethod
    def _should_run_drift(self):
        pass

    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.scenarios_dir = os.path.join(os.path.abspath(os.path.join(self.current_dir, '')), f'{self.get_provider_name()}/scenarios')
        self.supported_versions = os.listdir(self.scenarios_dir)
        self.test_files = []
        if not os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION')):
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    def _copy_module_dir(self, version: str, module_path: str, working_dir: str):
        moudle_dir_src = self._get_module_dir_path(version, module_path)
        shutil.copytree(moudle_dir_src, working_dir)

    def _get_module_dir_path(self, version: str, module_path: str) -> str:
        if not os.path.isdir(os.path.join(self.scenarios_dir, version, module_path)):
            version_dir = 'cross_version'
        else:
            version_dir = version
        return os.path.join(self.scenarios_dir, version_dir, module_path)

    # pylint: disable=consider-using-with
    def run_test_case(self, module_path: str, assert_func, base_scanner_data_for_iac: Optional[str], test_options: TestOptions):

        module_path = '{}/{}'.format(self.get_component(), module_path)
        if test_options.run_drift_detection:
            self._run_drift_detection_for_terraform(module_path)
            self._run_drift_detection_for_cloudformation(module_path, test_options.cfn_template_params)

        if test_options.run_cloudformation:
            self._run_cloudformation_test_case(module_path, assert_func, test_options.cfn_template_params, base_scanner_data_for_iac)

        if test_options.run_cloudmapper:
            self._safe_execute('cloudmapper', self._run_cloudmapper_test_case, module_path, assert_func)

        if test_options.run_terraform:
            version = test_options.tf_version if test_options.tf_version else 'latest'
            self._safe_execute(f'terraform_{version}',
                               self._run_terraform_test_case_for_version,
                               module_path,
                               assert_func,
                               version,
                               base_scanner_data_for_iac,
                               test_options.expected_exception)

    def _run_terraform_test_case_for_version(self,
                                             module_path: str,
                                             assert_func,
                                             version,
                                             base_scanner_data_for_iac: Optional[str],
                                             expected_exception: Type[Exception] = None):
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        try:
            print('Running test for version {}'.format(version))
            self._validate_module(self._get_module_dir_path(version, module_path))
            self._copy_module_dir(version, module_path, working_dir)
            current_path = os.path.dirname(os.path.realpath(__file__))
            base_scanner_data_for_iac = os.path.join(current_path, '..', 'testing-accounts-data',
                                                     base_scanner_data_for_iac or 'account-data-vpc-platform')
            plan_json = os.path.join(self._get_module_dir_path(version, module_path), 'cached_plan.json')
            result = TerraformShowOutputTransformer.transform(plan_json,
                                                              '',
                                                              self.get_supported_services(),
                                                              self.DUMMY_SALT)

            output_path = self._save_result_to_file(json.dumps(result), os.path.join(working_dir, 'output.json'))
            exception_raised = False
            try:
                context = self.build_context(base_scanner_data_for_iac, output_path)
            except Exception as ex:
                if not (expected_exception and isinstance(ex, expected_exception)):
                    traceback.print_tb(ex.__traceback__, limit=None, file=None)
                    raise ex
                exception_raised = True

            if not exception_raised and expected_exception:
                raise Exception(f'An exception of type {expected_exception.__name__} was expected to be raised')
            if not expected_exception:
                assert_func(self, context)
        finally:
            if os.path.isdir(working_dir):
                shutil.rmtree(working_dir, ignore_errors=True)

    def _run_cloudmapper_test_case(self, module_path: str, assert_func):
        working_dir = None
        try:
            print('Running test for cloud mapper')
            working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            shutil.copytree(os.path.join(self.scenarios_dir, 'cross_version', module_path), working_dir)
            account_data_dir = os.path.join(working_dir, 'account-data')
            account_data_zip = f'{account_data_dir}.zip'
            if not os.path.isfile(account_data_zip):
                raise Exception('missing cloud mapper zip {}'.format(account_data_zip))
            shutil.unpack_archive(account_data_zip, extract_dir=account_data_dir, format='zip')
            context = self.build_context(account_data_dir, None)
            assert_func(self, context)
        finally:
            shutil.rmtree(working_dir, ignore_errors=True)

    def _run_cloudformation_test_case(self, module_path: str, assert_func, cfn_template_params: dict, base_scanner_data_for_iac: Optional[str]):
        print('Running cloudformation test case')
        scenario_folder = os.path.join(self.scenarios_dir, 'cross_version', module_path)
        template_file = os.path.join(scenario_folder, 'cloudformation.yaml')
        current_path = os.path.dirname(os.path.realpath(__file__))

        if base_scanner_data_for_iac:
            scanner_account_data_folder = os.path.join(current_path, '..', 'testing-accounts-data', base_scanner_data_for_iac)
        else:
            scanner_account_data_folder = os.path.join(current_path, 'aws', 'scenarios', 'cross_version', module_path, 'cfn-account-data')
            if not os.path.isdir(scanner_account_data_folder):
                scanner_account_data_folder = os.path.join(current_path, '..', 'testing-accounts-data', 'account-data-vpc-platform')

        if os.path.isfile(template_file):
            context = EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                           IacType.CLOUDFORMATION).build(account_data_dir_path=scanner_account_data_folder,
                                                                                         iac_file_path=template_file,
                                                                                         account_id=self.DUMMY_ACCOUNT_ID,
                                                                                         stack_name='testCfnStack',
                                                                                         region='us-east-1',
                                                                                         cfn_template_params=cfn_template_params or {},
                                                                                         salt=self.DUMMY_SALT)
            assert_func(self, context)

    def _run_drift_detection_for_terraform(self, module_path: str):
        if not self._should_run_drift():
            print(f'skipping drift for {module_path}')
            return
        print('Running drift detection for terraform')
        TerraformResourceFinder.initialize()
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        scenario_folder = os.path.join(self.scenarios_dir, 'cross_version', module_path)
        shutil.copytree(scenario_folder, working_dir)
        template_file_for_drift = os.path.join(working_dir, 'cloudformation.yaml')
        account_data_for_drift_path = os.path.join(working_dir, 'account-data-for-drift-cloudformation')
        try:
            if not os.path.isfile(template_file_for_drift) or not os.path.isfile(account_data_for_drift_path):
                logging.info(f'missing cloudformation.yaml or account-data-for-drift-cloudformation.zip for {scenario_folder}')
                return
            shutil.unpack_archive(account_data_for_drift_path + '.zip', extract_dir=account_data_for_drift_path, format='zip')
            result = self._find_drifts(account_data_for_drift_path, template_file_for_drift, self.DUMMY_ACCOUNT_ID, IacType.TERRAFORM).drifts
            self.assertEqual(result, [], "found drifts which means tf object and cm objects are different\n."
                                         " drifts are: {}".format(json.dumps([dataclasses.asdict(r) for r in result], indent=4)))
        finally:
            TerraformResourceFinder.destroy()
            shutil.rmtree(working_dir, ignore_errors=True)

    def _run_drift_detection_for_cloudformation(self, module_path: str, cfn_template_params: dict):
        if not self._should_run_drift():
            print(f'skipping drift for {module_path}')
            return
        print('Running drift detection for cloudformation')
        TerraformResourceFinder.initialize()
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        scenario_folder = os.path.join(self.scenarios_dir, 'cross_version', module_path)
        shutil.copytree(scenario_folder, working_dir)
        cloudformation_template = os.path.join(working_dir, 'cloudformation.yaml')
        account_data_for_drift_path = os.path.join(working_dir, 'account-data-for-drift-cloudformation')
        try:
            if not os.path.isfile(cloudformation_template) or not os.path.isfile(account_data_for_drift_path):
                logging.info(f'missing cloudformation.yaml for {scenario_folder}')
                return
            shutil.unpack_archive(account_data_for_drift_path + '.zip', extract_dir=account_data_for_drift_path, format='zip')
            result = self._find_drifts(account_data_for_drift_path, cloudformation_template, self.DUMMY_ACCOUNT_ID, IacType.CLOUDFORMATION,
                                       cfn_template_params, 'testCfnStack').drifts
            self.assertEqual(result, [], "found drifts which means cfn object and cm objects are different\n."
                                         " drifts are: {}".format(json.dumps([dataclasses.asdict(r) for r in result], indent=4)))
        finally:
            shutil.rmtree(working_dir, ignore_errors=True)

    def _find_drifts(self, cloud_mapper_dir: str, iac_file: str, account_id: str, iac_type: IacType,
                     cfn_template_params: Optional[dict] = None, workspace_name: Optional[str] = None) -> DriftDetectionResult:
        workspace_name = workspace_name or 'workspace'
        context_builder = self.create_context_builder_factory(iac_type)
        scanner_context = context_builder.build(cloud_mapper_dir,
                                                None,
                                                self.DUMMY_ACCOUNT_ID,
                                                ignore_exceptions=True,
                                                run_enrichment_requiring_aws=False,
                                                salt=self.DUMMY_SALT,
                                                **self.context_builder_extra_args)
        output_path = self.transform_cached_plan(iac_file) if iac_type == IacType.TERRAFORM else iac_file
        iac_file_before = output_path if iac_type == IacType.TERRAFORM else self.find_cloudformation_workspace_template(iac_file,
                                                                                                                        cloud_mapper_dir,
                                                                                                                        workspace_name)
        iac_context_before = context_builder.build(cloud_mapper_dir,
                                                   iac_file_before,
                                                   account_id,
                                                   use_after_data=False,
                                                   ignore_exceptions=True,
                                                   run_enrichment_requiring_aws=False,
                                                   salt=self.DUMMY_SALT,
                                                   stack_name=workspace_name,
                                                   region='us-east-1',
                                                   cfn_template_params=cfn_template_params or {},
                                                   **self.context_builder_extra_args)
        iac_context_after = context_builder.build(None,
                                                  output_path,
                                                  account_id,
                                                  use_after_data=True,
                                                  keep_deleted_entities=False,
                                                  ignore_exceptions=True,
                                                  run_enrichment_requiring_aws=False,
                                                  salt=self.DUMMY_SALT,
                                                  stack_name=workspace_name,
                                                  region='us-east-1',
                                                  cfn_template_params=cfn_template_params or {},
                                                  **self.context_builder_extra_args)
        drift_detector = EnvironmentContextDriftDetectorFactory.get(self.cloud_provider)
        drifts = drift_detector.find_drifts(scanner_context, iac_context_before, iac_context_after, workspace_name)
        return drifts

    @staticmethod
    def find_cloudformation_workspace_template(iac_file, account_data_dir_path, workspace_name) -> tuple:
        def get_subfolders_names(path: str):
            return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

        cfn_template = CloudformationUtils.load_cfn_template(iac_file)
        region = cfn_template.get('cr_extra_params', {}).get('region', 'us-east-1')
        for account in get_subfolders_names(account_data_dir_path):
            expected_template_file_path = os.path.join(account_data_dir_path, account, region,
                                                       'cloudformation-get-template', f'StackName-{workspace_name}.json')
            if os.path.isfile(expected_template_file_path):
                return expected_template_file_path, region
        raise Exception('did not find cloudformation template in account_data')

    def transform_cached_plan(self, iac_file):
        result = TerraformShowOutputTransformer.transform(iac_file,
                                                          '',
                                                          self.get_supported_services(),
                                                          self.DUMMY_SALT)
        output_path = self._save_result_to_file(json.dumps(result), os.path.join(iac_file.replace('cached_plan_for_drift.json', ''),
                                                                                 'output.json'))
        return output_path

    @staticmethod
    def _safe_execute(sub_case: str, func, *params):
        try:
            TerraformResourceFinder.initialize()
            func(*params)
        except Exception as ex:
            if hasattr(ex, 'msg'):
                ex.msg = ('Error in {}:: {}'.format(sub_case, ex.msg))
                raise ex
            traceback.print_tb(ex.__traceback__, limit=None, file=None)
            raise Exception('Error in {}:: {}'.format(sub_case, str(ex)))
        finally:
            TerraformResourceFinder.destroy()

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(result)
        return dest_path

    def _validate_module(self, module_path):
        files = file_utils.get_all_files(module_path)
        for file_path in files:
            if file_path.endswith('.tf'):
                with open(file_path, 'r') as file:
                    text = file.read()
                if f'provider "{self.get_provider_name()}' in text:
                    if 'alias =' not in text:
                        raise Exception('remove provider block from tf file')

    @abstractmethod
    def create_context_builder_factory(self, iac_type: IacType = IacType.TERRAFORM) -> Type[BaseEnvironmentContextBuilder]:
        pass
