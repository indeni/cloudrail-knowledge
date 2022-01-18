from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpClusterDiskType
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestContainerNodePool(GcpContextTest):
    def get_component(self):
        return 'container_node_pool'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        node_pool = next((np for np in ctx.container_node_pools if np.name in ('terraform-20220118113538134400000001',
                                                                               'google_container_node_pool.cluster6_nodepool_1.name')), None)
        self.assertIsNotNone(node_pool)
        self.assertEqual(node_pool.cluster, 'gke-cluster-006')
        self.assertEqual(node_pool.location, 'us-west1-a')
        self.assertTrue(node_pool.autoscaling)
        self.assertEqual(node_pool.autoscaling.max_node_count, 2)
        self.assertEqual(node_pool.autoscaling.min_node_count, 1)
        self.assertTrue(node_pool.management)
        self.assertTrue(node_pool.management.auto_repair)
        self.assertTrue(node_pool.management.auto_upgrade)
        self.assertEqual(node_pool.node_config.disk_size_gb, 10)
        self.assertEqual(node_pool.node_config.disk_type, GcpClusterDiskType.PD_STANDARD)
        self.assertFalse(node_pool.node_config.gcfs_enabled)
        self.assertEqual(node_pool.node_config.image_type, 'COS_CONTAINERD')
        self.assertEqual(node_pool.node_config.machine_type, 'e2-small')
