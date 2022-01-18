from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerClusterNetworkConfigProvider, \
    GcpContainerClusterWorkloadMetadataConfigMode, GcpContainerClusterReleaseChannel
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestContainerCluster(GcpContextTest):
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
        self.assertEqual(cluster.network_policy.provider, GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED)
        self.assertTrue(cluster.network_policy.enabled)

    @context(module_path="cluster_with_private_cluster_config")
    def test_cluster_with_private_cluster_config(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertIsNotNone(cluster.private_cluster_config)
        self.assertTrue(cluster.private_cluster_config.enable_private_endpoint)
        self.assertTrue(cluster.private_cluster_config.enable_private_nodes)
        self.assertFalse(cluster.private_cluster_config.master_global_access_config)

    @context(module_path="with_metadata")
    def test_with_metadata(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertIsNotNone(cluster.node_config.metadata)
        self.assertEqual(cluster.node_config.metadata, {"disable-legacy-endpoints": "true", "some_test": "true"})
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertIsNotNone(second_cluster.node_config.metadata)
        self.assertEqual(second_cluster.node_config.metadata, {"disable-legacy-endpoints": "false"})

    @context(module_path="with_secure_boot")
    def test_with_secure_boot(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.node_config.shielded_instance_config.enable_secure_boot)
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertFalse(second_cluster.node_config.shielded_instance_config.enable_secure_boot)

    @context(module_path="with_workload_metadata_config")
    def test_with_workload_metadata_config(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.node_config.workload_metadata_config_mode, GcpContainerClusterWorkloadMetadataConfigMode.MODE_UNSPECIFIED)
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertEqual(second_cluster.node_config.workload_metadata_config_mode, GcpContainerClusterWorkloadMetadataConfigMode.GCE_METADATA)

    @context(module_path="with_release_channel")
    def test_with_release_channel(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.release_channel, GcpContainerClusterReleaseChannel.REGULAR)
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertEqual(second_cluster.release_channel, GcpContainerClusterReleaseChannel.RAPID)

    @context(module_path="with_service_account")
    def test_with_service_account(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-001'), None)
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.node_config.service_account, 'default')
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-002'), None)
        self.assertIsNotNone(second_cluster)
        if second_cluster.is_managed_by_iac:
            self.assertEqual(second_cluster.node_config.service_account, 'google_service_account.new_service_account1.email')
        else:
            self.assertEqual(second_cluster.node_config.service_account, 'non-default-svc-001@dev-for-tests.iam.gserviceaccount.com')

    @context(module_path="with_master_auth")
    def test_with_master_auth(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertFalse(cluster.issue_client_certificate)
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertTrue(second_cluster.issue_client_certificate)

    @context(module_path="with_pod_security")
    def test_with_pod_security(self, ctx: GcpEnvironmentContext):
        cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-005'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.pod_security_policy_enabled)
        second_cluster = next((cluster for cluster in ctx.container_cluster if cluster.name == 'gke-cluster-006'), None)
        self.assertIsNotNone(second_cluster)
        self.assertFalse(second_cluster.pod_security_policy_enabled)
