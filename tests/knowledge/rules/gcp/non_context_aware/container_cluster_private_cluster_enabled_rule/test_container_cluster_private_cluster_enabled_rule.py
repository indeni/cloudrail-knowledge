from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_private_cluster_enabled_rule import ContainerClusterPrivateClusterEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterPrivateClusterEnabledRule(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterPrivateClusterEnabledRule()

    @rule_test('both_disabled', should_alert=True, number_of_issue_items=2)
    def test_both_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('both_enabled', should_alert=False)
    def test_both_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('one_enabled', should_alert=True)
    def test_one_enabled(self, rule_result: RuleResponse):
        pass
