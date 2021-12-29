from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import DataLakeAnalyticsDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestDataLakeAnalyticsDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return DataLakeAnalyticsDiagnosticLogsEnabledRule()

    @rule_test('dl_analytics_diagnostic_not_enabled', should_alert=True)
    def test_dl_analytics_diagnostic_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('dl_analytics_diagnostic_enabled', should_alert=False)
    def test_dl_analytics_diagnostic_enabled(self, rule_result: RuleResponse):
        pass
