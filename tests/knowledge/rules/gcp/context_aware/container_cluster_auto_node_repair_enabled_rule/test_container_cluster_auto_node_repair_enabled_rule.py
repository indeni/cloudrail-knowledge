from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.container_cluster_auto_node_repair_enabled_rule import ContainerClusterAutoNodeRepairEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterAutoNodeRepairEnabledRule(GcpBaseRuleTest):
    def get_rule(self):
        return ContainerClusterAutoNodeRepairEnabledRule()

    @rule_test('no_clusters_compliant', should_alert=True, number_of_issue_items=2)
    def test_no_clusters_compliant(self, rule_result: RuleResponse):
        pass

    @rule_test('both_clusters_compliant', should_alert=False)
    def test_both_clusters_compliant(self, rule_result: RuleResponse):
        pass

    @rule_test('one_cluster_compliant', should_alert=True)
    def test_one_cluster_compliant(self, rule_result: RuleResponse):
        pass
