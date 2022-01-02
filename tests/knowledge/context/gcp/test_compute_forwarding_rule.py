from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeForwardingRule(GcpContextTest):
    def get_component(self):
        return 'compute_forwarding_rule'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_forwarding_rules if compute.name == 'ssh-forwarding'), None)
        self.assertIsNotNone(compute)
        self.assertEqual(compute.port_range.port_ranges, [(22, 22)])
        if compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.target, 'https://www.googleapis.com/compute/v1/projects/dev-for-tests/regions/us-west1/targetPools/default-tp')
        else:
            self.assertEqual(compute.target, 'google_compute_target_pool.default.self_link')
