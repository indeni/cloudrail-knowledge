from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestDaxCluster(AwsContextTest):

    def get_component(self):
        return "dax_clusters"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.dax_cluster), 1)
        for dax_cluster in ctx.dax_cluster:
            self.assertEqual(dax_cluster.cluster_name, 'encrypted')
            self.assertTrue(dax_cluster.server_side_encryption)
            self.assertEqual(dax_cluster.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/dynamodb/home?region=us-east-1#cache-cluster:selected=encrypted')

    @context(module_path="non_encrypted_cluster")
    def test_non_encrypted_cluster(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.dax_cluster), 1)
        for dax_cluster in ctx.dax_cluster:
            self.assertEqual(dax_cluster.cluster_name, 'non-encrypt')
            self.assertFalse(dax_cluster.server_side_encryption)
            self.assertTrue(dax_cluster.cluster_arn)
            self.assertFalse(dax_cluster.tags)

    @context(module_path="with_tags")
    def test_non_encrypted_cluster_with_tags(self, ctx: AwsEnvironmentContext):
        dax = next((dax for dax in ctx.dax_cluster if dax.cluster_name == 'non-encrypt'), None)
        self.assertIsNotNone(dax)
        self.assertTrue(dax.cluster_arn)
        self.assertTrue(dax.tags)
        self.assertFalse(dax.server_side_encryption)
