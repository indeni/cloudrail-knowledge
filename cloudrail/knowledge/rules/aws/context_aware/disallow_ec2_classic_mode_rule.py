from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class DisallowEc2ClassicModeRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'disallow_ec2_classic_mode_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for redshift in env_context.redshift_clusters:
            if not redshift.is_ec2_vpc_platform:
                issues.append(
                    Issue(
                        f'~{redshift.get_type()}~. '
                        f'{redshift.get_type()} with database name `{redshift.get_friendly_name()}` is using EC2-Classic mode.'
                        f' It should use EC2-VPC mode instead',
                        redshift,
                        redshift))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
