from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_release_channel_enabled_rule import ContainerClusterReleaseChannelEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterReleaseChannelEnabledRule(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterReleaseChannelEnabledRule()

    @rule_test('both_channels_incorrect', should_alert=True, number_of_issue_items=2)
    def test_both_channels_incorrect(self, rule_result: RuleResponse):
        pass

    @rule_test('both_channels_correct', should_alert=False)
    def test_both_channels_correct(self, rule_result: RuleResponse):
        pass

    @rule_test('one_channel_incorrect', should_alert=True)
    def test_one_channel_incorrect(self, rule_result: RuleResponse):
        pass
