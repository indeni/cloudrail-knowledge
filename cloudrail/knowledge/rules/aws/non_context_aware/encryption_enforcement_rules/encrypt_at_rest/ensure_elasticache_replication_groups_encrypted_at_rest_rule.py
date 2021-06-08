from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureElasticacheReplicationGroupsEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_elasticache_replication_group_encrypt_at_rest_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for elasticache_replication_group in env_context.elasti_cache_replication_groups:
            if elasticache_replication_group.is_new_resource():
                if not elasticache_replication_group.encrypted_at_rest:
                    issues.append(
                        Issue(
                            f'The {elasticache_replication_group.get_type()} `{elasticache_replication_group.get_friendly_name()}` is '
                            f'not set to use encryption at rest', elasticache_replication_group, elasticache_replication_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.elasti_cache_replication_groups)
