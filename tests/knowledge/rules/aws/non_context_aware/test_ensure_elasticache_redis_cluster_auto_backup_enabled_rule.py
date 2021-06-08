import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.elasticache.elasticache_cluster import ElastiCacheCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_elasticache_redis_cluster_auto_backup_enabled_rule import \
    EnsureElasticacheRedisClusterAutoBackupEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureElasticacheRedisClusterAutoBackupEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticacheRedisClusterAutoBackupEnabledRule()

    def test_non_car_elasticache_redis_cluster_automatic_backup_turned_on_fail(self):
        # Arrange
        elasticache_cluster: ElastiCacheCluster = create_empty_entity(ElastiCacheCluster)
        elasticache_cluster.engine = 'redis'
        elasticache_cluster.snapshot_retention_limit = 0
        context = AwsEnvironmentContext(elasticache_clusters=[elasticache_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_elasticache_redis_cluster_automatic_backup_turned_on_pass(self):
        # Arrange
        elasticache_cluster: ElastiCacheCluster = create_empty_entity(ElastiCacheCluster)
        elasticache_cluster.engine = 'redis'
        elasticache_cluster.snapshot_retention_limit = 5
        context = AwsEnvironmentContext(elasticache_clusters=[elasticache_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_elasticache_redis_cluster_automatic_backup_turned_on__not_reids_engine__pass(self):
        # Arrange
        elasticache_cluster: ElastiCacheCluster = create_empty_entity(ElastiCacheCluster)
        elasticache_cluster.engine = 'memcached'
        elasticache_cluster.snapshot_retention_limit = 0
        context = AwsEnvironmentContext(elasticache_clusters=[elasticache_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
