from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import SearchServiceDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestSearchServiceDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return SearchServiceDiagnosticLogsEnabledRule()

    @rule_test('search_diagnostic_not_enabled', should_alert=True)
    def test_search_diagnostic_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('search_diagnostic_enabled', should_alert=False)
    def test_search_diagnostic_enabled(self, rule_result: RuleResponse):
        pass
