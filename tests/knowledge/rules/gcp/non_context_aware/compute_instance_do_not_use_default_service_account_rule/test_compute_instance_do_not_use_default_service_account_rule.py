from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_rule import ComputeInstanceDoNotUseDefaultServiceAccountRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceDoNotUseDefaultServiceAccountRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceDoNotUseDefaultServiceAccountRule()

    @rule_test('both_default', should_alert=True, number_of_issue_items=2)
    def test_both_default(self, rule_result: RuleResponse):
        pass

    @rule_test('no_default', should_alert=False)
    def test_no_default(self, rule_result: RuleResponse):
        pass

    @rule_test('one_default', should_alert=True)
    def test_one_default(self, rule_result: RuleResponse):
        pass
