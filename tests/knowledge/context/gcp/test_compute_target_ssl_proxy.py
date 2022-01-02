from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeTargetSslProxy(GcpContextTest):
    def get_component(self):
        return 'compute_target_ssl_proxy'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_ssl_proxy if compute.name == 'test-proxy'), None)
        self.assertIsNotNone(compute)
        self.assertIsNotNone(compute.ssl_policy)
        if compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.backend_service, "https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/backendServices/backend-service")
            self.assertEqual(compute.ssl_certificates, ["https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/sslCertificates/default-cert"])
            self.assertEqual(compute.ssl_policy_identifier, "https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/sslPolicies/ssl-policy")
        elif compute.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(compute.backend_service, "google_compute_backend_service.default.id")
            self.assertEqual(compute.ssl_certificates, ["google_compute_ssl_certificate.default.id"])
            self.assertEqual(compute.ssl_policy_identifier, "ssl-policy")

    @context(module_path="ssl_policy_none")
    def test_ssl_policy_none(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_target_ssl_proxy if compute.name == 'test-proxy'), None)
        self.assertIsNotNone(compute)
        self.assertIsNone(compute.ssl_policy)
        if compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.backend_service, "https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/backendServices/backend-service")
            self.assertEqual(compute.ssl_certificates, ["https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/sslCertificates/default-cert"])
        elif compute.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(compute.backend_service, "google_compute_backend_service.default.id")
            self.assertEqual(compute.ssl_certificates, ["google_compute_ssl_certificate.default.id"])
