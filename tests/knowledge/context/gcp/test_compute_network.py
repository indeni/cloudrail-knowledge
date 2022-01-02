from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeNetwork(GcpContextTest):
    def get_component(self):
        return 'compute_network'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_networks if compute.name == 'new-network'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.auto_create_subnetworks)
        self.assertEqual(compute.routing_mode.value, 'GLOBAL')

    @context(module_path="subnetworks")
    def test_subnetworks(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_networks if compute.name == 'vpc-network-3'), None)
        self.assertIsNotNone(compute)
        self.assertEqual(len(compute.subnetworks), 2)
