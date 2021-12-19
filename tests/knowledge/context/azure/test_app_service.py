from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAppService(AzureContextTest):

    def get_component(self):
        return "app_service"

    @context(module_path="ftps_state/all_allowed")
    def test_ftps_state_all_allowed(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertEqual(app_service.app_service_config.ftps_state, FtpsState.ALL_ALLOWED)

    @context(module_path="ftps_state/disabled")
    def test_ftps_state_disabled(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertEqual(app_service.app_service_config.ftps_state, FtpsState.DISABLED)

    @context(module_path="ftps_state/ftps_only")
    def test_ftps_state_ftps_only(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertEqual(app_service.app_service_config.ftps_state, FtpsState.FTPS_ONLY)

    @context(module_path="ftps_state/not_specified_in_tf")
    def test_ftps_state_not_specified_in_tf(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertEqual(app_service.app_service_config.ftps_state, FtpsState.ALL_ALLOWED)

    # ------------------- auth_enable tests -------------------

    @context(module_path="auth_settings/auth_enable")
    def test_auth_enable(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1a-webapp')
        self.assertEqual(app_service.app_service_config.auth_settings.enabled, True)

    @context(module_path="auth_settings/auth_disable")
    def test_auth_disable(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa2a-webapp')
        self.assertEqual(app_service.app_service_config.auth_settings.enabled, False)

    # ------------------- TLS tests -------------------

    @context(module_path="tls/webapp_tls_1_1")
    def test_tls_1_1(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2272-tls-1-1-webapp')
        self.assertEqual(app_service.app_service_config.minimum_tls_version, '1.1')

    @context(module_path="tls/webapp_tls_1_2")
    def test_tls_1_2(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2272-tls-1-2-webapp')
        self.assertEqual(app_service.app_service_config.minimum_tls_version, '1.2')

    @context(module_path="tls/webapp_tls_missing")
    def test_tls_missing(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2272-tls-missing-webapp')
        self.assertEqual(app_service.app_service_config.minimum_tls_version, '1.2')

    # ------------------- https only tests -------------------

    @context(module_path="https_only/https_only_set_to_true")
    def test_https_only_set_to_true(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        self.assertEqual(app_service.https_only, True)

    @context(module_path="https_only/https_only_set_to_false")
    def test_https_only_set_to_false(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        self.assertEqual(app_service.https_only, False)

    @context(module_path="https_only/https_only_is_missing")
    def test_https_only_set_is_missing(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2300-https-only-webapp')
        self.assertEqual(app_service.https_only, False)

    # ------------------- client certificates test -------------------

    @context(module_path="client_certificates/webapp_client_cert_enabled")
    def test_client_cert_enabled(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertTrue(app_service.client_cert_required)

    @context(module_path="client_certificates/webapp_client_cert_not_enabled")
    def test_client_cert_not_enabled(self, ctx: AzureEnvironmentContext):
        app_service = self._get_app_service(ctx, 'cr2152wa1-webapp')
        self.assertFalse(app_service.client_cert_required)

    def _get_app_service(self, ctx: AzureEnvironmentContext, app_service_name: str) -> AzureAppService:
        app_service = next((app_service for app_service in ctx.app_services if app_service.server_name == app_service_name), None)
        self.assertIsNotNone(app_service)
        return app_service
