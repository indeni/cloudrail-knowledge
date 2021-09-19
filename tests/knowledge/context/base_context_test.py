import dataclasses
import json
import os
import shutil
import tempfile
import traceback
import unittest
import uuid
from abc import abstractmethod
from typing import Any, Dict, Optional, Type

import semantic_version
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.drift_detection.drift_detection_result import DriftDetectionResult
from cloudrail.knowledge.drift_detection.environment_context_drift_detector_factory import EnvironmentContextDriftDetectorFactory
from cloudrail.knowledge.utils import file_utils
from semantic_version import SimpleSpec, Version

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

    def _generate_main_tf_for_module(self, version: str, working_dir: str):
        main_path = os.path.join(working_dir, 'main.tf')
        if version == 'latest':
            main_text = self.get_latest_provider_block()
        else:
            main_text = self.get_version_provider_block(version[1:])
        with open(main_path, 'a') as file:
            file.write(main_text)

        self.test_files.append(main_path)

    # pylint: disable=consider-using-with
    def run_test_case(self, module_path: str, assert_func, base_scanner_data_for_iac: Optional[str], test_options: TestOptions):

        module_path = '{}/{}'.format(self.get_component(), module_path)
        if test_options.run_drift_detection:
            self._run_drift_detection(module_path)

        self._run_cloudformation_test_case(module_path, assert_func, test_options.cfn_template_params, base_scanner_data_for_iac)

        if test_options.run_cloudmapper:
            self._safe_execute('cloudmapper', self._run_cloudmapper_test_case, module_path, assert_func)

        if test_options.run_terraform:
            if test_options.tf_version is None:
                tf_version_to_run = [version for version in self.supported_versions if semantic_version.validate(version[1:])]
            elif test_options.tf_version == '':
                tf_version_to_run = []
            else:
                versions = SimpleSpec(test_options.tf_version.replace('v', ''))
                tf_version_to_run = [version for version in self.supported_versions if semantic_version.validate(version[1:])
                                     and versions.match(Version(version[1:]))]
            if test_options.run_latest_provider:
                tf_version_to_run.append('latest')
            if test_options.run_terraform:  # test_options.use_cached_plan_data_ratio == 100: # TODO why?
                tf_version_to_run = tf_version_to_run[0:1]

            for version in tf_version_to_run:
                sub_case = 'terraform_{}'.format(version)
                self._safe_execute(sub_case,
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
            self._generate_main_tf_for_module(version, working_dir)
            current_path = os.path.dirname(os.path.realpath(__file__))
            base_scanner_data_for_iac = os.path.join(current_path, '..', 'testing-accounts-data',
                                                     base_scanner_data_for_iac or 'account-data-vpc-platform')
            cached_plan = os.path.join(self._get_module_dir_path(version, module_path), 'filtered_plan.json')
            output_path = shutil.copy2(cached_plan, os.path.join(working_dir, 'output.json'))
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
        try:
            TerraformResourceFinder.initialize()
            scenario_folder = os.path.join(self.scenarios_dir, 'cross_version', module_path)
            template_file = os.path.join(scenario_folder, 'cloudformation.yaml')
            current_path = os.path.dirname(os.path.realpath(__file__))

            if base_scanner_data_for_iac:
                scanner_account_data_folder = os.path.join(current_path, '..', 'testing-accounts-data', base_scanner_data_for_iac)
            else:
                scanner_account_data_folder = os.path.join(current_path, 'aws', 'scenarios', 'cross_version', module_path, 'account-data')
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
        finally:
            TerraformResourceFinder.destroy()

    def _run_drift_detection(self, module_path: str):
        print('Running drift detection')
        TerraformResourceFinder.initialize()
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        scenario_folder = os.path.join(self.scenarios_dir, 'cross_version', module_path)
        shutil.copytree(scenario_folder, working_dir)
        cached_plan_for_drift_path = os.path.join(working_dir, 'filtered_plan_for_drift.json')
        account_data_for_drift_path = os.path.join(working_dir, 'account-data-for-drift')
        try:
            if not os.path.isfile(cached_plan_for_drift_path):
                print(f'missing cached_plan_for_drift.json for {scenario_folder}')
                return
            shutil.unpack_archive(account_data_for_drift_path + '.zip', extract_dir=account_data_for_drift_path, format='zip')
            result = self._find_drifts(account_data_for_drift_path, cached_plan_for_drift_path, self.DUMMY_ACCOUNT_ID).drifts
            self.assertEqual(result, [], "found drifts which means tf object and cm objects are different\n."
                                         " drifts are: {}".format(json.dumps([dataclasses.asdict(r) for r in result], indent=4)))
        finally:
            TerraformResourceFinder.destroy()
            shutil.rmtree(working_dir, ignore_errors=True)

    def _find_drifts(self, cloud_mapper_dir: str, terraform_file: str, account_id: str) -> DriftDetectionResult:
        context_builder = self.create_context_builder_factory()
        scanner_context = context_builder.build(cloud_mapper_dir,
                                                None,
                                                self.DUMMY_ACCOUNT_ID,
                                                self.DUMMY_SALT,
                                                ignore_exceptions=True,
                                                run_enrichment_requiring_aws=False)
        output_path = shutil.copy2(terraform_file, os.path.join(terraform_file.replace('filtered_plan_for_drift.json', ''),
                                                                'output.json'))
        iac_context_before = context_builder.build(None,
                                                   output_path,
                                                   account_id,
                                                   self.DUMMY_SALT,
                                                   use_after_data=False,
                                                   ignore_exceptions=True,
                                                   run_enrichment_requiring_aws=False,
                                                   **self.context_builder_extra_args)
        iac_context_after = context_builder.build(None,
                                                  output_path,
                                                  account_id,
                                                  self.DUMMY_SALT,
                                                  use_after_data=True,
                                                  keep_deleted_entities=False,
                                                  ignore_exceptions=True,
                                                  run_enrichment_requiring_aws=False,
                                                  **self.context_builder_extra_args)
        return EnvironmentContextDriftDetectorFactory.get(CloudProvider.AMAZON_WEB_SERVICES).find_drifts(scanner_context, iac_context_before,
                                                                                                         iac_context_after, 'workspace')

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
    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        pass
