from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeGlobalForwardingRule(GcpContextTest):
    def get_component(self):
        return 'compute_global_forwarding_rule'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_global_forwarding_rule if
                        compute.name == 'test-global-https-forwarding-rule'), None)
        self.assertIsNone(compute)

    @context(module_path="with_targets")
    def test_with_targets(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_global_forwarding_rule if
                        compute.name == 'test-global-forwarding-rule'), None)
        self.assertIsNotNone(compute)
        self.assertIsNotNone(compute.target)
        self.assertTrue(compute.target_identifier in ['google_compute_target_ssl_proxy.test.id',
                                                      'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/targetSslProxies/test-ssl-proxy'])
