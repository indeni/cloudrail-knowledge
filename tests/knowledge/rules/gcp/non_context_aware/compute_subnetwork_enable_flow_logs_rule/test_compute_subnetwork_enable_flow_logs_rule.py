from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_subnetwork_enable_flow_logs_rule import ComputeSubNetworkEnableFlowLogsRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeSubNetworkEnableFlowLogsRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeSubNetworkEnableFlowLogsRule()

    @rule_test('both_with_flow_logs', should_alert=False)
    def test_both_with_flow_logs(self, rule_result: RuleResponse):
        pass

    @rule_test('one_with_flow_logs', should_alert=True)
    def test_one_with_flow_logs(self, rule_result: RuleResponse):
        pass

    @rule_test('without_flow_logs', should_alert=True, number_of_issue_items=2)
    def test_without_flow_logs(self, rule_result: RuleResponse):
        pass
