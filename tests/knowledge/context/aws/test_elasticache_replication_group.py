from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestElastiCacheReplicationGroup(AwsContextTest):

    def get_component(self):
        return "elasticache/elasticache_repliaction_group"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        for elasti_cache in ctx.elasti_cache_replication_groups:
            self.assertTrue(elasti_cache.encrypted_at_rest)
            self.assertEqual(elasti_cache.replication_group_id, 'tf-rep-group-1-encrypted')
            self.assertFalse(elasti_cache.encrypted_in_transit)
            self.assertEqual(elasti_cache.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/elasticache/home?region=us-east-1'
                             '#redis-group-nodes:id=tf-rep-group-1-encrypted;clusters')

    @context(module_path="no_encryption_at_rest")
    def test_no_encryption_at_rest(self, ctx: AwsEnvironmentContext):
        for elasti_cache in ctx.elasti_cache_replication_groups:
            self.assertFalse(elasti_cache.encrypted_at_rest)
            self.assertEqual(elasti_cache.replication_group_id, 'tf-rep-group-1-non-encrypted')
            self.assertFalse(elasti_cache.encrypted_in_transit)

    @context(module_path="encrypted_in_transit", base_scanner_data_for_iac='account-data-elasticache-default-network')
    def test_encrypted_in_transit(self, ctx: AwsEnvironmentContext):
        for elasti_cache in ctx.elasti_cache_replication_groups:
            self.assertFalse(elasti_cache.encrypted_at_rest)
            self.assertEqual(elasti_cache.replication_group_id, 'tf-rep-group-1-encrypted')
            self.assertTrue(elasti_cache.encrypted_in_transit)
            self.assertTrue(elasti_cache.is_in_default_vpc)
            self.assertEqual(elasti_cache.subnet_group_name, 'default')
            self.assertEqual(len(elasti_cache.elasticache_subnet_ids), 6)
            self.assertEqual(elasti_cache.elasticache_security_group_ids, ['sg-37970008'])

    @context(module_path="secure_replication_group_with_networking")
    def test_secure_replication_group_with_networking(self, ctx: AwsEnvironmentContext):
        rep_group = next((rep_group for rep_group in ctx.elasti_cache_replication_groups if rep_group.name == 'tf-rep-group-1-encrypted'), None)
        self.assertIsNotNone(rep_group)
        self.assertTrue(rep_group.encrypted_at_rest)
        self.assertTrue(rep_group.encrypted_in_transit)
        self.assertEqual(rep_group.subnet_group_name, 'tf-test-cache-subnet')
        self.assertEqual(len(rep_group.elasticache_security_group_ids), 1)
        self.assertFalse(rep_group.is_in_default_vpc)
        self.assertTrue(rep_group.elasticache_subnet_ids)
