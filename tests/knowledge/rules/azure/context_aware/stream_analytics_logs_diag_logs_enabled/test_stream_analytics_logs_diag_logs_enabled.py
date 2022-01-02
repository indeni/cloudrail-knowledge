from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import StreamAnalyitcsJobDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestStreamAnalyitcsJobDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return StreamAnalyitcsJobDiagnosticLogsEnabledRule()

    @rule_test('stream_analytics_diagnostic_not_enabled', should_alert=True)
    def test_stream_analytics_diagnostic_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('stream_analytics_diagnostic_enabled', should_alert=False)
    def test_stream_analytics_diagnostic_enabled(self, rule_result: RuleResponse):
        pass
