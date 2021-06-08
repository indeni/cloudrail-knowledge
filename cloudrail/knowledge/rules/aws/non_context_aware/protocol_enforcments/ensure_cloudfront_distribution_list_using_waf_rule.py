from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class CloudFrontEnsureWafUsedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudfront_distribution_using_waf'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for distribution_list in env_context.cloudfront_distribution_list:
            if not distribution_list.is_waf_enabled:
                issues.append(
                    Issue(
                        f'The {distribution_list.get_type()} `{distribution_list.get_friendly_name()}` is not using a WAF Web ACL',
                        distribution_list, distribution_list))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloudfront_distribution_list)
