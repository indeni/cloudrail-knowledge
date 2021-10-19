from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_diagnostic_logs_enabled_in_app_services_rule import AppServiceDiagnosticLogsRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceDiagnosticLogsRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceDiagnosticLogsRule()

    @rule_test('webapp_all_logging_enabled', should_alert=False)
    def test_logs_all_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_only_error_logging_enabled', should_alert=True)
    def test_logs_only_error_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_only_http_logging_enabled', should_alert=True)
    def test_logs_only_http_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_only_tracing_enabled', should_alert=True)
    def test_logs_only_tracing_enabled(self, rule_result: RuleResponse):
        pass
