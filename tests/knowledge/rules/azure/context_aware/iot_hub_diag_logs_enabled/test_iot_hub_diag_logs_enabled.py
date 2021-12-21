from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import IotHubDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestIotHubDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return IotHubDiagnosticLogsEnabledRule()

    @rule_test('iot_hub_diagnostic_not_enabled', should_alert=True)
    def test_iot_hub_diagnostic_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('iot_hub_diagnostic_enabled', should_alert=False)
    def test_iot_hub_diagnostic_enabled(self, rule_result: RuleResponse):
        pass
