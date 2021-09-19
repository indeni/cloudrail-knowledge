from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestDocdbCluster(AwsContextTest):

    def get_component(self):
        return "docdb_clusters"

    @context(module_path="docdb_clusters_encrypted_at_rest")
    def test_docdb_clusters_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        cluster_data = ctx.docdb_cluster[0]
        self.assertEqual(cluster_data.cluster_identifier, 'my-docdb-cluster')
        self.assertEqual(cluster_data.storage_encrypted, True)
        self.assertFalse(cluster_data.tags)
        self.assertEqual(cluster_data.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/docdb/home?region=us-east-1#cluster-details/my-docdb-cluster')

    @context(module_path="docdb_cluster_non_encrypted_in_transit")
    def test_docdb_clusters_non_encrypted_in_transit(self, ctx: AwsEnvironmentContext):
        cluster_data = ctx.docdb_cluster[0]
        encryption_state = 'enabled'
        for parameter_group in ctx.docdb_cluster_parameter_groups:
            self.assertFalse(parameter_group.tags)
            for parameter in parameter_group.parameters:
                if parameter_group.group_name == 'in-transit-encryp-disabled' and parameter.parameter_name == 'tls':
                    encryption_state = parameter.parameter_value
        self.assertEqual(cluster_data.cluster_identifier, 'in-transit-encryp-disabled')
        self.assertEqual(encryption_state, 'disabled')

    @context(module_path="docdb_cluster_encrypted_in_transit")
    def test_docdb_clusters_encrypted_in_transit(self, ctx: AwsEnvironmentContext):
        cluster_data = ctx.docdb_cluster[0]
        encryption_state = 'enabled'
        for parameter_group in ctx.docdb_cluster_parameter_groups:
            for parameter in parameter_group.parameters:
                if parameter_group.group_name == 'default.docdb3.6' and parameter.parameter_name == 'tls':
                    encryption_state = parameter.parameter_value
        self.assertEqual(cluster_data.cluster_identifier, 'in-transit-encryp-enabled')
        self.assertEqual(encryption_state, 'enabled')

    @context(module_path="docdb_cluster_encrypted_at_rest_with_kms_key")
    def test_docdb_cluster_encrypted_at_rest_with_kms_key(self, ctx: AwsEnvironmentContext):
        for cluster_data in ctx.docdb_cluster:
            if cluster_data.cluster_identifier == 'my-docdb-cluster-test2':
                self.assertEqual(cluster_data.storage_encrypted, True)
                self.assertEqual(cluster_data.kms_key_id, 'arn:aws:kms:us-east-1:115553109071:key/033a057a-dd81-4bcd-b919-3a1f89e088ef')
                self.assertFalse(cluster_data.enabled_cloudwatch_logs_exports)

    @context(module_path="with_tags")
    def test_docdb_cluster_non_encrypted_with_tags(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.docdb_cluster
                        if cluster.cluster_identifier == 'in-transit-encryp-disabled'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.tags)
        cluster_param = next((param for param in ctx.docdb_cluster_parameter_groups
                              if param.group_name == 'in-transit-encryp-disabled'), None)
        self.assertIsNotNone(cluster_param)
        self.assertTrue(cluster_param.tags)

    @context(module_path="docdb_cluster_with_logs_exports")
    def test_docdb_cluster_with_logs_exports(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.docdb_cluster
                        if cluster.cluster_identifier == 'docdb-no-logging'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(len(cluster.enabled_cloudwatch_logs_exports) == 2)
