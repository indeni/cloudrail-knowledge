from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.auto_provisioning_log_analytics_agent_disabled_rule import \
    AutoProvisioningLogAnalyticsAgentDisabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureNoUnusedSecurityGroupsRule(AzureBaseRuleTest):

    def get_rule(self):
        return AutoProvisioningLogAnalyticsAgentDisabledRule()

    @rule_test('auto_provisioning_on', should_alert=False)
    def test_auto_provisioning_on(self, rule_result: RuleResponse):
        pass

    @rule_test('auto_provisioning_off', should_alert=True)
    def test_auto_provisioning_off(self, rule_result: RuleResponse):
        pass
