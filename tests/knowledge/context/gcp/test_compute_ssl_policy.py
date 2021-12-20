from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeSslPolicy(GcpContextTest):
    def get_component(self):
        return 'compute_ssl_policy'

    @context(module_path="basic")
    def test_compute_ssl_policy_production(self, ctx: GcpEnvironmentContext):
        compute = self.find_compute_by_name(ctx, "production-ssl-policy")
        self.assertEqual(compute.min_tls_version, "TLS_1_0")
        self.assertEqual(compute.profile, "MODERN")
        self.assertIsNone(compute.custom_features)

    @context(module_path="basic")
    def test_compute_ssl_policy_no_prod(self, ctx: GcpEnvironmentContext):
        compute = self.find_compute_by_name(ctx, "nonprod-ssl-policy")
        self.assertEqual(compute.min_tls_version, "TLS_1_2")
        self.assertEqual(compute.profile, "MODERN")
        self.assertIsNone(compute.custom_features)

    @context(module_path="basic")
    def test_compute_ssl_policy_custom(self, ctx: GcpEnvironmentContext):
        compute = self.find_compute_by_name(ctx, "custom-ssl-policy")
        self.assertEqual(compute.min_tls_version, "TLS_1_2")
        self.assertEqual(compute.profile, "CUSTOM")
        self.assertEqual(compute.custom_features, ["TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"])

    def find_compute_by_name(self, ctx: GcpEnvironmentContext, compute_name: str):
        compute = next((compute for compute in ctx.compute_ssl_policy if compute.name == compute_name), None)
        self.assertIsNotNone(compute)
        return compute
