from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_ensure_no_ip_forwarding_rule import \
    ComputeInstanceEnsureNoIpForwardingRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceEnsureNoIpForwardingRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceEnsureNoIpForwardingRule()

    @rule_test('both_can_ip_forward', should_alert=True, number_of_issue_items=2)
    def test_compute_instance_ensure_no_ip_forwarding_with_both_can_ip_forward(self, rule_result: RuleResponse):
        pass

    @rule_test('none_can_ip_forward', should_alert=False)
    def test_compute_instance_ensure_no_ip_forwarding_none_can_ip_forward(self, rule_result: RuleResponse):
        pass

    @rule_test('one_can_ip_forward', should_alert=True)
    def test_compute_instance_ensure_no_ip_forwarding_one_can_ip_forward(self, rule_result: RuleResponse):
        pass
