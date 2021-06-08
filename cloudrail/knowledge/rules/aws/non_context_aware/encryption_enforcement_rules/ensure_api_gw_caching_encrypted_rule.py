from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureApiGwCachingEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_api_gateway_caching_encrypted'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for api_gw in env_context.rest_api_gw:
            if api_gw.method_settings and api_gw.method_settings.caching_enabled and not api_gw.method_settings.caching_encrypted:
                issues.append(
                    Issue(f"The {api_gw.get_type()} `{api_gw.get_id()}` has caching enabled and not encrypted for "
                          f"method `{api_gw.method_settings.http_method.value}` in the stage `{api_gw.method_settings.stage_name}`", api_gw, api_gw))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rest_api_gw)
