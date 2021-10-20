from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test
from cloudrail.knowledge.rules.azure.non_context_aware.unused_network_security_group_rule import UnusedNetworkSecurityGroupRule


class TestEnsureNoUnusedSecurityGroupsRule(AzureBaseRuleTest):

    def get_rule(self):
        return UnusedNetworkSecurityGroupRule()

    @rule_test('nsg_unused', should_alert=True)
    def test_nsg_unused(self, rule_result: RuleResponse):
        pass

    @rule_test('nsg_attached_to_subnet', should_alert=False)
    def test_nsg_attached_to_subnet(self, rule_result: RuleResponse):
        pass

    @rule_test('nsg_attached_to_nic', should_alert=False)
    def test_nsg_attached_to_nic(self, rule_result: RuleResponse):
        pass
