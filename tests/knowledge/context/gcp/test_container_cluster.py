from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerClusterNetworkConfigProvider
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlDatabaseInstance(GcpContextTest):
    def get_component(self):
        return 'container_cluster'

    @context(module_path="cluster_with_labels")
    def test_cluster_with_labels(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'kuber'), None)
        self.assertIsNotNone(cluster)
        self.assertIsNotNone(cluster.labels)
        self.assertTrue(key in ('foo_1') for key in cluster.labels.keys())

    @context(module_path="cluster_with_optional")
    def test_cluster_with_optional(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'kuber'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.location, 'us-central1-a')
        self.assertTrue(cluster.enable_shielded_nodes)
        self.assertIsNotNone(cluster.master_authorized_networks_config)
        self.assertIsNotNone(cluster.master_authorized_networks_config.cidr_blocks)
        self.assertEqual(cluster.master_authorized_networks_config.cidr_blocks[0].cidr_block, '0.0.0.0/0')
        self.assertEqual(cluster.master_authorized_networks_config.cidr_blocks[0].display_name, 'office')
        self.assertIsNotNone(cluster.authenticator_groups_config)
        self.assertEqual(cluster.authenticator_groups_config.security_group, 'gke-security-groups@indeni.com')
        if cluster.origin == EntityOrigin.TERRAFORM:
            self.assertIsNone(cluster.cluster_ipv4_cidr)
        elif cluster.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(cluster.cluster_ipv4_cidr, '10.1.0.0/20')

    @context(module_path="cluster_without_optional")
    def test_cluster_without_optional(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'kuber-2'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.location, 'us-central1-a')
        self.assertFalse(cluster.enable_shielded_nodes)
        self.assertIsNone(cluster.master_authorized_networks_config)
        self.assertIsNone(cluster.authenticator_groups_config)
        if cluster.origin == EntityOrigin.TERRAFORM:
            self.assertIsNone(cluster.cluster_ipv4_cidr)
        elif cluster.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(cluster.cluster_ipv4_cidr, '10.2.0.0/20')

    @context(module_path="cluster_with_network_policy_enabled")
    def test_cluster_with_network_policy_enabled(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.network_config.provider, GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED)
        self.assertTrue(cluster.network_config.enabled)
