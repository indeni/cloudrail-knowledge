from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_fsx_windows_file_system_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for fsx_windows_file_system in env_context.fsx_windows_file_systems:
            if fsx_windows_file_system.is_new_resource():
                if not fsx_windows_file_system.kms_data or fsx_windows_file_system.kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The FSx Windows File System `{fsx_windows_file_system.get_friendly_name()}` is not set to be encrypted at rest using customer-managed CMK',
                            fsx_windows_file_system, fsx_windows_file_system))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.fsx_windows_file_systems)
