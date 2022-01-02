from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import EventHubNamespaceDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEventHubNamespaceDiagnosticLogs(AzureBaseRuleTest):

    def get_rule(self):
        return EventHubNamespaceDiagnosticLogsEnabledRule()

    @rule_test('monitor_settings_enabled', should_alert=False)
    def test_monitor_settings_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('monitor_settings_disabled', should_alert=True)
    def test_monitor_settings_disabled(self, rule_result: RuleResponse):
        pass
