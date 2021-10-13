from cloudrail.knowledge.rules.azure.non_context_aware.auto_provisioning_log_analytics_agent_disabled_rule import \
    AutoProvisioningLogAnalyticsAgentDisabledRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestEnsureNoUnusedSecurityGroupsRule(AzureBaseRuleTest):

    def get_rule(self):
        return AutoProvisioningLogAnalyticsAgentDisabledRule()

    def test_auto_provisioning_on(self):
        self.run_test_case('auto_provisioning_on', should_alert=False)

    def test_auto_provisioning_off(self):
        self.run_test_case('auto_provisioning_off', should_alert=True)
