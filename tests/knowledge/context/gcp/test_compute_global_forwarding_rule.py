from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestComputeGlobalForwardingRule(GcpContextTest):
    def get_component(self):
        return 'compute_global_forwarding_rule'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_global_forwarding_rule if
                        compute.name == 'test-global-https-forwarding-rule'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.target in ['google_compute_global_forwarding_rule.https-forwarding.target',
                                           'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/targetHttpsProxies/test-proxy'])
        compute = next((compute for compute in ctx.compute_global_forwarding_rule if
                       compute.name == 'test-global-ssl-forwarding-rule'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.target in ['google_compute_global_forwarding_rule.ssl-forwarding.target',
                                           'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/targetSslProxies/test-ssl-proxy'])

