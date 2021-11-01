from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestElastiCacheCluster(AwsContextTest):

    def get_component(self):
        return "elasticache/elasticache_cluster"

    @context(module_path="basic_default", base_scanner_data_for_iac='account-data-elasticache-default-network.zip')
    def test_basic_default(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-example'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.arn)
        self.assertEqual(cluster.subnet_group_name, 'default')
        self.assertTrue(cluster.is_in_default_vpc)
        self.assertEqual(len(cluster.elasticache_security_group_ids), 1)
        self.assertEqual(cluster.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/elasticache/home?region=us-east-1#redis-nodes:id=cluster-example')
        self.assertEqual(len(cluster.elasticache_subnet_ids), 6)
        self.assertTrue(cluster.snapshot_retention_limit == 0)

    @context(module_path="basic_networking")
    def test_basic_networking(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-example'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.arn)
        self.assertEqual(cluster.subnet_group_name, 'tf-test-cache-subnet')
        self.assertFalse(cluster.is_in_default_vpc)
        self.assertTrue(cluster.elasticache_security_group_ids)
        self.assertTrue(cluster.elasticache_subnet_ids)

    @context(module_path="default_under_replication_group", base_scanner_data_for_iac='account-data-elasticache-default-network.zip')
    def test_default_under_replication_group(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-example'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.arn)
        self.assertEqual(cluster.replication_group_id, 'tf-rep-group-1-encrypted')
        self.assertEqual(cluster.elasticache_security_group_ids, ['sg-37970008'])
        self.assertEqual(len(cluster.elasticache_subnet_ids), 6)

    @context(module_path="under_replication_group_tf_using_reference_with_id", base_scanner_data_for_iac='account-data-elasticache-default-network.zip')
    def test_under_replication_group_tf_using_reference_with_id(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-example'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.arn)
        self.assertTrue(cluster.replication_group_id in ('tf-rep-group-1-encrypted', 'aws_elasticache_replication_group.cloudrail.id'))
        self.assertTrue(cluster.elasticache_security_group_ids)
        self.assertEqual(len(cluster.elasticache_subnet_ids), 6)
        self.assertEqual(cluster.engine, 'redis')

    @context(module_path="networking_under_replication_group")
    def test_networking_under_replication_group(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-example'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.arn)
        self.assertEqual(cluster.replication_group_id, 'tf-rep-group-1-encrypted')
        self.assertTrue(cluster.elasticache_security_group_ids)
        self.assertEqual(len(cluster.elasticache_subnet_ids), 2)
        self.assertEqual(cluster.engine, 'redis')

    @context(module_path="auto_backup_enabled", base_scanner_data_for_iac='account-data-elasticache-default-network.zip')
    def test_auto_backup_enabled(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-test-bck-enabled'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.snapshot_retention_limit > 0)
        self.assertEqual(cluster.engine, 'redis')

    @context(module_path="auto-backup-disabled-with-param", base_scanner_data_for_iac='account-data-elasticache-default-network.zip')
    def test_auto_backup_disabled_with_param(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.elasticache_clusters if cluster.cluster_name == 'cluster-test-bck-disabled'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.snapshot_retention_limit == 0)
