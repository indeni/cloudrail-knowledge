from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudWatchLogGroupsRetentionUsageRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cw_log_group_no_retention'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for log_group in env_context.cloud_watch_log_groups:
            if not log_group.retention_in_days:
                issues.append(
                    Issue(
                        f'The {log_group.get_type()} `{log_group.get_friendly_name()}` does not have a retention policy set'
                        , log_group, log_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloud_watch_log_groups)
