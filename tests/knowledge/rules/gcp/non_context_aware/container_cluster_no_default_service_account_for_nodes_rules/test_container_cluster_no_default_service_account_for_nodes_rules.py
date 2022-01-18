from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_no_default_service_account_for_nodes_rules import \
    ContainerClusterNoDefaultServiceAccountForNodesRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterNoDefaultServiceAccountForNodesRule(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterNoDefaultServiceAccountForNodesRule()

    @rule_test('both_non_default', should_alert=False)
    def test_both_non_default(self, rule_result: RuleResponse):
        pass

    @rule_test('both_default', should_alert=True, number_of_issue_items=2)
    def test_both_default(self, rule_result: RuleResponse):
        pass

    @rule_test('one_default', should_alert=True)
    def test_one_default(self, rule_result: RuleResponse):
        pass
