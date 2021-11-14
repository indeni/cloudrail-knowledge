from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestComputeNetwork(GcpContextTest):
    def get_component(self):
        return 'compute_network'

    @context(module_path="basic", test_options=TestOptions(use_cached_plan_data_ratio=0, run_drift_detection=False))
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_network if compute.name == 'new-network'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.auto_create_subnetworks)
        self.assertEqual(compute.routing_mode, 'GLOBAL')
        self.assertTrue(compute.delete_default_routes_on_create)
        self.assertEqual(compute.project, 'dev-for-tests')


