from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class StorageBucketLoggingEnabledRule(GcpBaseRule):

    def get_id(self) -> str:
        return 'non_car_storage_bucket_ensure_logging_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for bucket in env_context.storage_buckets:
            if not bucket.logging_enable:
                issues.append(Issue(f'The Google {bucket.get_type()} `{bucket.get_friendly_name()}` logging is not enabled.',
                              bucket,
                              bucket))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.storage_buckets)
