from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_diagnostic_logs_enabled_in_app_services_rule import AppServiceDiagnosticLogsRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceDiagnosticLogsRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceDiagnosticLogsRule()

    def test_logs_all_logging_enabled(self):
        self.run_test_case('webapp_all_logging_enabled', should_alert=False)

    def test_logs_only_error_logging_enabled(self):
        self.run_test_case('webapp_only_error_logging_enabled', should_alert=True)

    def test_logs_only_http_logging_enabled(self):
        self.run_test_case('webapp_only_http_logging_enabled', should_alert=True)

    def test_logs_only_tracing_enabled(self):
        self.run_test_case('webapp_only_tracing_enabled', should_alert=True)
