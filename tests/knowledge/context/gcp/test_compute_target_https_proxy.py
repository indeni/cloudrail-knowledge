from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestComputeNetwork(GcpContextTest):
    def get_component(self):
        return 'compute_target_https_proxy'

    @context(module_path="with_ssl_policy")
    def test_with_ssl_policy(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_https_proxy if compute.name == 'test-proxy'), None)
        self.assertIsNotNone(compute)
        self.assertIsNotNone(compute.ssl_policy)

    @context(module_path="without_ssl_policy")
    def test_without_ssl_policy(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_https_proxy if compute.name == 'test-proxy'), None)
        self.assertIsNotNone(compute)
        self.assertIsNone(compute.ssl_policy)
