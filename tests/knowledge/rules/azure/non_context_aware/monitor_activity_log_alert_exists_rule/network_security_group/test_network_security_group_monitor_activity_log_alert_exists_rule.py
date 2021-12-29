from cloudrail.knowledge.rules.azure.non_context_aware.monitor_activity_log_alert_exists_rule import NetworkSecurityGroupMonitorActivityLogAlertExistsRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestANetworkSecurityGroupMonitorActivityLogAlertExistsRule(AzureBaseRuleTest):
    def get_rule(self):
        return NetworkSecurityGroupMonitorActivityLogAlertExistsRule()

    @rule_test('operation_missing', should_alert=True)
    def test_operation_missing(self, rule_result: RuleResponse):
        pass

    @rule_test('monitor_disabled', should_alert=True)
    def test_monitor_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('category_missing', should_alert=True)
    def test_category_missing(self, rule_result: RuleResponse):
        pass

    @rule_test('monitor_exists', should_alert=False)
    def test_monitor_exists(self, rule_result: RuleResponse):
        pass
