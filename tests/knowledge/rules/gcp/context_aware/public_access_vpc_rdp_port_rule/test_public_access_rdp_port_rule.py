from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.public_access_vpc_port_rule import PublicAccessVpcRdpPortRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPublicAccessVpcRdpPortRule(GcpBaseRuleTest):
    def get_rule(self):
        return PublicAccessVpcRdpPortRule()

    @rule_test('unrestricted_and_pub_ip', should_alert=True)
    def test_unrestricted_and_pub_ip(self, rule_result: RuleResponse):
        self.assertEqual(len(rule_result.issues), 1)
        self.assertTrue('with one of the public IP addresses' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Virtual Machine Instance')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Compute Firewall')

    @rule_test('unrestricted_priv_ip_with_lb', should_alert=True)
    def test_unrestricted_priv_ip_with_lb(self, rule_result: RuleResponse):
        self.assertEqual(len(rule_result.issues), 1)
        self.assertTrue('exposed via load balancer' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Virtual Machine Instance')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Compute Firewall')

    @rule_test('restricted_rdp', should_alert=False)
    def test_restricted_rdp(self, rule_result: RuleResponse):
        pass
