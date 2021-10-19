from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CacheBehavior
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudfrontDistributionFieldLevelEncryptionRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudfront_distribution_field_level_encryption_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for distribution in env_context.cloudfront_distribution_list:
            if distribution.is_new_resource():
                ordered_list = self._make_ordered_list(distribution.get_ordered_behavior_list())
                default_cache = distribution.get_default_behavior()
                if not default_cache.field_level_encryption_id and not ordered_list:
                    issues.append(
                        Issue(
                            f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use "
                            f"Field Level Encryption to protect "
                            f"data in transit in default_cache_behavior", distribution, distribution))
                elif default_cache.field_level_encryption_id and ordered_list:
                    issues.append(
                        Issue(
                            f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use Field Level Encryption to protect"
                            f" data in transit in {ordered_list}", distribution, distribution))
                elif not default_cache.field_level_encryption_id and ordered_list:
                    issues.append(
                        Issue(
                            f"The {distribution.get_type()} `{distribution.get_friendly_name()}` is not set to use Field Level Encryption to protect"
                            f" data in transit in default_cache_behavior"
                            f" and in {ordered_list}", distribution, distribution))
        return issues

    @staticmethod
    def _make_ordered_list(ordered_cache_list: List[CacheBehavior]) -> List:
        return [f'ordered_cache_behavior #{cache.precedence}' for cache in ordered_cache_list if cache.field_level_encryption_id is None]

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.cloudfront_distribution_list)
