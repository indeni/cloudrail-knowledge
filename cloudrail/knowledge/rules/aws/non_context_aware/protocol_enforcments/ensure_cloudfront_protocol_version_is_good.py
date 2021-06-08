from typing import List, Dict

from packaging import version

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class CloudFrontEnsureVersionRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudfront_protocol_version'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for distribution_list in env_context.cloudfront_distribution_list:
            if self._version_check(distribution_list.viewer_cert.minimum_protocol_version):
                issues.append(
                    Issue(
                        f'The {distribution_list.get_type()} `{distribution_list.get_friendly_name()}` is set to use a minimum protocol version'
                        f' of `{distribution_list.viewer_cert.minimum_protocol_version}` whereas TLSv1.2_2019 is the recommended '
                        f'minimum', distribution_list, distribution_list))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloudfront_distribution_list)

    @staticmethod
    def _version_check(proto_version: str) -> bool:
        if proto_version != 'SSLv3':
            version_num = proto_version.replace('TLSv', '').replace('_', '.')
            return version.parse(version_num) < version.parse('1.2.2019')
        else:
            return True
