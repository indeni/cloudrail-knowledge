from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType

class EnsureCloudtrailTrailExists(AwsBaseRule):

    @staticmethod
    def filter_non_iac_managed_issues() -> bool:
        return False

    def get_id(self) -> str:
        return 'ensure_cloudtrail_trail_exists'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for account in env_context.accounts:
            if not env_context.cloudtrail:
                issues.append(
                    Issue(
                        f'The account `{account.get_friendly_name()}` does not have at least one Cloudtrail trail enabled',
                        account, account ))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.accounts)
