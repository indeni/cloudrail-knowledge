from typing import List, Dict
from packaging import version

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


# Currently only checking API GW V1 (rest API's), as V2 does not support but TLS v1.2.


class EnsureApiGwUseModernTlsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_api_gateway_tls'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for api_gw in env_context.rest_api_gw:
            if api_gw.domain and self._version_check(api_gw.domain.security_policy):
                issues.append(
                    Issue(f"The {api_gw.get_type()} `{api_gw.get_friendly_name()}` "
                          f"has a domain configured but not enforcing TLS v1.2 ", api_gw, api_gw.domain))
        return issues

    @staticmethod
    def _version_check(proto_version: str) -> bool:
        version_num = proto_version.replace('TLS_', '').replace('_', '.')
        return version.parse(version_num) < version.parse('1.2')

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rest_api_gw)
