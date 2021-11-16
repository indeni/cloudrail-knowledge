from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestComputeNetwork(GcpContextTest):
    def get_component(self):
        return 'compute_target_http_proxy'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_http_proxy if compute.name == 'test-proxy'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.url_map in ['google_compute_target_http_proxy.default.url_map', 'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/urlMaps/url-map'])


