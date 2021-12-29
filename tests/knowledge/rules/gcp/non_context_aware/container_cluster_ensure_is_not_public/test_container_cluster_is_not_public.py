from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_is_not_public_rule import ContainerClusterIsNotPublictRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterIsNotPublic(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterIsNotPublictRule()

    @rule_test('both_private', should_alert=False)
    def test_both_private(self, rule_result: RuleResponse):
        pass

    @rule_test('both_public', should_alert=True, number_of_issue_items=2)
    def test_both_public(self, rule_result: RuleResponse):
        pass

    @rule_test('one_public', should_alert=True)
    def test_one_public(self, rule_result: RuleResponse):
        pass
