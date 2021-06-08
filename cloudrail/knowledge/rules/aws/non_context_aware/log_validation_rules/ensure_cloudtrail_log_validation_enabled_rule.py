from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudTrailLogValidationEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_aws_cloudtrail_log_validation_disabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for trail in env_context.cloudtrail:
            if not trail.log_file_validation:
                issues.append(
                    Issue(
                        f'The {trail.get_type()} trail `{trail.get_friendly_name()}` does not have log validation enabled'
                        , trail, trail))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloudtrail)
