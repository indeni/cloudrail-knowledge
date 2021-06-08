from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureElasticacheRedisClusterAutoBackupEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_elasticache_redis_cluster_automatic_backup_turned_on'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for elasticache_cluster in env_context.elasticache_clusters:
            if elasticache_cluster.engine == 'redis' and elasticache_cluster.snapshot_retention_limit == 0:
                issues.append(
                    Issue(
                        f'The {elasticache_cluster.get_type()} `{elasticache_cluster.get_friendly_name()}` has automatic backups turned off',
                        elasticache_cluster, elasticache_cluster))
            return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.elasticache_clusters)
