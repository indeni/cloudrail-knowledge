from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestNeptuneCluster(AwsContextTest):

    def get_component(self):
        return "neptune_clusters"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        for neptune_cluster in ctx.neptune_clusters:
            self.assertTrue(neptune_cluster.encrypted_at_rest)
            self.assertTrue(neptune_cluster.arn)
            self.assertEqual(neptune_cluster.cluster_identifier, 'cloudrail-test-encrypted')
            self.assertEqual(neptune_cluster.port, 8182)
            self.assertTrue(neptune_cluster.cluster_id)
            self.assertFalse(neptune_cluster.cloudwatch_logs_exports)
            self.assertEqual(neptune_cluster.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/neptune/home?region=us-east-1#database:id=cloudrail-test-encrypted;is-cluster=true')

    @context(module_path="not_encrypted_at_rest")
    def test_not_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        for neptune_cluster in ctx.neptune_clusters:
            self.assertFalse(neptune_cluster.encrypted_at_rest)
            self.assertTrue(neptune_cluster.arn)
            self.assertEqual(neptune_cluster.cluster_identifier, 'cloudrail-test-not-encrypted')
            self.assertEqual(neptune_cluster.port, 8182)
            self.assertTrue(neptune_cluster.cluster_id)

    @context(module_path="encrypted_at_rest_with_aws_managed_cmk", base_scanner_data_for_iac='account-data-ssm-param-kms-keys.zip')
    def test_encrypted_at_rest_with_aws_managed_cmk(self, ctx: AwsEnvironmentContext):
        for neptune_cluster in ctx.neptune_clusters:
            self.assertTrue(neptune_cluster.encrypted_at_rest)
            self.assertTrue(neptune_cluster.arn)
            self.assertEqual(neptune_cluster.cluster_identifier, 'cloudrail-test-encrypted')
            self.assertNotEqual(neptune_cluster.kms_data.key_manager.value, 'CUSTOMER')
            self.assertNotEqual(neptune_cluster.kms_data.key_manager.name, 'CUSTOMER')
            self.assertEqual(neptune_cluster.port, 8182)
            self.assertTrue(neptune_cluster.cluster_id)

    @context(module_path="encrypted_at_rest_with_customer_managed_cmk")
    def test_encrypted_at_rest_with_customer_managed_cmk(self, ctx: AwsEnvironmentContext):
        for neptune_cluster in ctx.neptune_clusters:
            self.assertTrue(neptune_cluster.encrypted_at_rest)
            self.assertTrue(neptune_cluster.arn)
            self.assertEqual(neptune_cluster.cluster_identifier, 'cloudrail-test-encrypted')
            self.assertNotEqual(neptune_cluster.kms_data.key_manager.value, 'AWS')
            self.assertNotEqual(neptune_cluster.kms_data.key_manager.name, 'AWS')
            self.assertEqual(neptune_cluster.port, 8182)
            self.assertTrue(neptune_cluster.cluster_id)

    @context(module_path="vpc_non_default")
    def test_vpc_non_default(self, ctx: AwsEnvironmentContext):
        neptune_cluster = next((neptune_cluster for neptune_cluster in ctx.neptune_clusters
                                if neptune_cluster.cluster_identifier == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(neptune_cluster)
        self.assertTrue(neptune_cluster.encrypted_at_rest)
        self.assertTrue(neptune_cluster.arn)
        self.assertEqual(neptune_cluster.port, 8182)
        self.assertEqual(neptune_cluster.db_subnet_group_name, 'nondefault')
        self.assertTrue(neptune_cluster.security_group_ids)
        self.assertTrue(len(neptune_cluster.security_group_ids), 1)
        self.assertTrue(neptune_cluster.cluster_id)
        self.assertFalse(neptune_cluster.tags)

    @context(module_path="cluster_and_instance_with_tags", base_scanner_data_for_iac='account-data-vpc-platform.zip')
    def test_cluster_and_instance_with_tags(self, ctx: AwsEnvironmentContext):
        neptune_cluster = next((neptune_cluster for neptune_cluster in ctx.neptune_clusters
                                if neptune_cluster.cluster_identifier == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(neptune_cluster)
        self.assertTrue(neptune_cluster.tags)
        for instance in neptune_cluster.cluster_instances:
            self.assertTrue(instance.tags)

    @context(module_path="with_logs_export_enabled")
    def test_with_logs_export_enabled(self, ctx: AwsEnvironmentContext):
        neptune_cluster = next((neptune_cluster for neptune_cluster in ctx.neptune_clusters
                                if neptune_cluster.cluster_identifier == 'test-logging'), None)
        self.assertIsNotNone(neptune_cluster)
        self.assertEqual(neptune_cluster.cloudwatch_logs_exports, ["audit"])
