from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAthenaWorkgroupsEncryptionCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_athena_workgroup_query_results_encrypt_at_rest_using_customer_managed_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for workgroup in env_context.athena_workgroups:
            if workgroup.is_new_resource():
                if workgroup.encryption_option == 'SSE_S3' or (workgroup.kms_data and workgroup.kms_data.key_manager != KeyManager.CUSTOMER):
                    issues.append(
                        Issue(
                            f'The {workgroup.get_type()} `{workgroup.get_friendly_name()}` is set to use encrypt at rest '
                            f'but it is not using customer-managed CMKs', workgroup, workgroup))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.athena_workgroups)
