from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_metadata_server_enabled_rule import ContainerClusterMetadataServerEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterMetadataServerEnabledRule(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterMetadataServerEnabledRule()

    @rule_test('both_servers_correct', should_alert=False)
    def test_both_servers_correct(self, rule_result: RuleResponse):
        pass

    @rule_test('both_servers_incorrect', should_alert=True, number_of_issue_items=2)
    def test_both_servers_incorrect(self, rule_result: RuleResponse):
        pass

    @rule_test('one_server_correct', should_alert=True)
    def test_one_server_correct(self, rule_result: RuleResponse):
        pass
