from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class StorageBucketIsNotPubliclyAccessibleRule(GcpBaseRule):

    def get_id(self) -> str:
        return 'car_storage_bucket_ensure_no_anonymous_public_access'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for bucket in env_context.storage_buckets:
            if bucket.iam_policy and\
                any(member in ('allUsers', 'allAuthenticatedUsers') for binding in bucket.iam_policy.bindings for member in binding.members):
                issues.append(Issue(f'The Google {bucket.get_type()} `{bucket.get_friendly_name()}` is anonymously or publicly accessible.',
                              bucket,
                              bucket.iam_policy))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.storage_buckets)
