from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestMonitorDiagnosticSetting(AzureContextTest):

    def get_component(self):
        return "monitor_diagnostic_setting"

    @context(module_path="logs_and_retention_enabled")
    def test_logs_and_retention_enabled(self, ctx: AzureEnvironmentContext):
        diagnostic_settings = next((settings for settings in ctx.monitor_diagnostic_settings if settings.server_name == 'testing-keyvault'), None)
        self.assertIsNotNone(diagnostic_settings)
        self.assertTrue(diagnostic_settings.logs_settings.enabled)
        self.assertTrue(diagnostic_settings.logs_settings.retention_policy.enabled)
        self.assertEqual(diagnostic_settings.logs_settings.retention_policy.days, 31)

    @context(module_path="log_enabled_retention_disabled")
    def test_log_enabled_retention_disabled(self, ctx: AzureEnvironmentContext):
        diagnostic_settings = next((settings for settings in ctx.monitor_diagnostic_settings if settings.server_name == 'testing-keyvault'), None)
        self.assertIsNotNone(diagnostic_settings)
        self.assertTrue(diagnostic_settings.logs_settings.enabled)
        self.assertFalse(diagnostic_settings.logs_settings.retention_policy.enabled)
        self.assertEqual(diagnostic_settings.logs_settings.retention_policy.days, 31)

    @context(module_path="logs_not_defined")
    def test_logs_not_defined(self, ctx: AzureEnvironmentContext):
        diagnostic_settings = next((settings for settings in ctx.monitor_diagnostic_settings if settings.server_name == 'testing-keyvault'), None)
        self.assertIsNotNone(diagnostic_settings)
        self.assertIsNone(diagnostic_settings.logs_settings)

    @context(module_path="log_enabled_retention_days_default")
    def test_log_enabled_retention_days_default(self, ctx: AzureEnvironmentContext):
        diagnostic_settings = next((settings for settings in ctx.monitor_diagnostic_settings if settings.server_name == 'testing-keyvault'), None)
        self.assertIsNotNone(diagnostic_settings)
        self.assertTrue(diagnostic_settings.logs_settings.enabled)
        self.assertTrue(diagnostic_settings.logs_settings.retention_policy.enabled)
        self.assertEqual(diagnostic_settings.logs_settings.retention_policy.days, 0)
