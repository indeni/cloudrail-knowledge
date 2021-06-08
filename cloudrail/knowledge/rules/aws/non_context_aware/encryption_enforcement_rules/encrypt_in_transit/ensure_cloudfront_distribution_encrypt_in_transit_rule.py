from typing import List, Dict

from cloudrail.knowledge.context.aws.cloudfront.cloud_front_distribution_list import CacheBehavior
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudfrontDistributionEncryptInTransitRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudfront_distribution_encrypt_in_transit'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for distribution in env_context.cloudfront_distribution_list:
            default_behavior_restricted = self._is_https_restricted(distribution.get_default_behavior().viewer_protocol_policy)
            ordered_behavior_list = distribution.get_ordered_behavior_list()
            ordered_cache_list = self._get_messages(ordered_behavior_list)
            ordered_cache_restricted = len(ordered_cache_list) == 0

            if not default_behavior_restricted and ordered_cache_restricted:
                issues.append(
                    Issue(
                        f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use HTTPS to protect"
                        f" data in transit in default_cache_behavior", distribution, distribution))
            elif default_behavior_restricted and not ordered_cache_restricted:
                issues.append(
                    Issue(
                        f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use HTTPS to protect"
                        f" data in transit in {ordered_cache_list}", distribution, distribution))
            elif not (default_behavior_restricted or ordered_cache_restricted):
                issues.append(
                    Issue(
                        f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use HTTPS to protect"
                        f" data in transit default_cache_behavior"
                        f" and in {ordered_cache_list}", distribution, distribution))
        return issues

    @staticmethod
    def _is_https_restricted(protocol: str) -> bool:
        secure_values = ['redirect-to-https', 'https-only']
        return protocol in secure_values

    @classmethod
    def _get_messages(cls, ordered_behavior_list: List[CacheBehavior]) -> List[str]:
        return [f'ordered_cache_behavior #{cache.precedence}' for cache in ordered_behavior_list
                if not cls._is_https_restricted(cache.viewer_protocol_policy)]

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloudfront_distribution_list)
