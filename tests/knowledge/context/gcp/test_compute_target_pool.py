from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeTargetPool(GcpContextTest):
    def get_component(self):
        return 'compute_target_pool'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_pools if compute.server_name == 'default-tp'), None)
        self.assertIsNotNone(compute)
        if compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.instances, ['https://www.googleapis.com/compute/v1/projects/dev-for-tests/zones/us-west1-a/instances/restricted-gce'])
            self.assertEqual(compute.self_link, 'https://www.googleapis.com/compute/v1/projects/dev-for-tests/regions/us-west1/targetPools/default-tp')
        else:
            self.assertEqual(compute.instances, ['google_compute_instance.restricted-ssh.self_link'])
            self.assertEqual(compute.self_link, 'google_compute_target_pool.default.self_link')
