from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestAppServiceConfig(AzureContextTest):
    def get_component(self):
        return "app_service_config"

    @context(module_path="ftps_state/all_allowed", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_ftps_state_all_allowed(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertEqual(app_service_config.ftps_state, FtpsState.ALL_ALLOWED)

    @context(module_path="ftps_state/disabled", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_ftps_state_disabled(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertEqual(app_service_config.ftps_state, FtpsState.DISABLED)

    @context(module_path="ftps_state/ftps_only", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_ftps_state_ftps_only(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertEqual(app_service_config.ftps_state, FtpsState.FTPS_ONLY)

    @context(module_path="diagnostic_logs/webapp_all_logging_enabled")
    def test_logs_all_logging_enabled(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertTrue(app_service_config.logs.detailed_error_logging_enabled)
        self.assertTrue(app_service_config.logs.http_logging_enabled)
        self.assertTrue(app_service_config.logs.request_tracing_enabled)

    @context(module_path="diagnostic_logs/webapp_only_errorlogging_enabled")
    def test_logs_only_error_logging_enabled(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertTrue(app_service_config.logs.detailed_error_logging_enabled)
        self.assertFalse(app_service_config.logs.http_logging_enabled)
        self.assertFalse(app_service_config.logs.request_tracing_enabled)

    @context(module_path="diagnostic_logs/webapp_only_http_logging_enabled")
    def test_logs_only_http_logging_enabled(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertFalse(app_service_config.logs.detailed_error_logging_enabled)
        self.assertTrue(app_service_config.logs.http_logging_enabled)
        self.assertFalse(app_service_config.logs.request_tracing_enabled)

    @context(module_path="diagnostic_logs/webapp_only_tracing_enabled")
    def test_logs_only_tracing_enabled(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertFalse(app_service_config.logs.detailed_error_logging_enabled)
        self.assertFalse(app_service_config.logs.http_logging_enabled)
        self.assertTrue(app_service_config.logs.request_tracing_enabled)

    @context(module_path="diagnostic_logs/no_logs_in_app_service")
    def test_logs_not_define(self, ctx: AzureEnvironmentContext):
        app_service_config = self._get_app_service(ctx)
        self.assertFalse(app_service_config.logs.detailed_error_logging_enabled)
        self.assertFalse(app_service_config.logs.http_logging_enabled)
        self.assertFalse(app_service_config.logs.request_tracing_enabled)

    def _get_app_service(self, ctx: AzureEnvironmentContext) -> AzureAppServiceConfig:
        config = next((config for config in ctx.app_service_configs if config.server_name == 'cr2152wa1-webapp'), None)
        self.assertIsNotNone(config)
        return config
