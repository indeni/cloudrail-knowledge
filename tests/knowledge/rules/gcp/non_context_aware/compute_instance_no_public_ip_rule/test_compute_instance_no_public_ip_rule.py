from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_public_ip_rule import ComputeInstanceNoPublicIpRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceNoPublicIpRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceNoPublicIpRule()

    @rule_test('both_public_ip', should_alert=True, number_of_issue_items=2)
    def test_both_public_ip(self, rule_result: RuleResponse):
        pass

    @rule_test('one_public_ip', should_alert=True)
    def test_one_public_ip(self, rule_result: RuleResponse):
        pass

    @rule_test('no_public_ip', should_alert=False)
    def test_no_public_ip(self, rule_result: RuleResponse):
        pass
