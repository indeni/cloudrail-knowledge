from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest
from cloudrail.knowledge.rules.azure.non_context_aware.unused_network_security_group_rule import UnusedNetworkSecurityGroupRule


class TestEnsureNoUnusedSecurityGroupsRule(AzureBaseRuleTest):

    def get_rule(self):
        return UnusedNetworkSecurityGroupRule()

    def test_nsg_unused(self):
        self.run_test_case('nsg_unused',
                           should_alert=True)

    def test_nsg_attached_to_subnet(self):
        self.run_test_case('nsg_attached_to_subnet',
                           should_alert=False)

    def test_nsg_attached_to_nic(self):
        self.run_test_case('nsg_attached_to_nic',
                           should_alert=False)
