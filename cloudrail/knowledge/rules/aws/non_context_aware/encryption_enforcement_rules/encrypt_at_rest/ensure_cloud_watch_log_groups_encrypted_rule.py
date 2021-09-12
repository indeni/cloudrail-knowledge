from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudWatchLogGroupsEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_cloudwatch_log_group_encrypted_at_rest_using_kms_cmk'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for log_group in env_context.cloud_watch_log_groups:
            if log_group.is_new_resource():
                if not log_group.kms_encryption or log_group.kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The {log_group.get_type()} `{log_group.get_friendly_name()}` is set to use encrypt at rest '
                            f'but it is not using CMKs', log_group, log_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloud_watch_log_groups)
