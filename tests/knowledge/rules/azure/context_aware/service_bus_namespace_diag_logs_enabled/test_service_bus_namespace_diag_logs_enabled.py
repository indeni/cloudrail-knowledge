from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import ServiceBusNamespaceDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestServiceBusNamespaceDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return ServiceBusNamespaceDiagnosticLogsEnabledRule()

    @rule_test('servicebus_namespace_enabled', should_alert=False)
    def test_servicebus_namespace_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('servicebus_namespace_not_enabled', should_alert=True)
    def test_servicebus_namespace_not_enabled(self, rule_result: RuleResponse):
        pass
