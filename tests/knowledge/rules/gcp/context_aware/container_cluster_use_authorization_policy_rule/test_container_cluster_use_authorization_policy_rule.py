from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.container_cluster_use_authorization_policy_rule import ContainerClusterUseAuthorizationPolicyRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterUseAuthorizationPolicyRule(GcpBaseRuleTest):
    def get_rule(self):
        return ContainerClusterUseAuthorizationPolicyRule()

    @rule_test('both_disabled', should_alert=True, number_of_issue_items=2)
    def test_both_disabled(self, rule_result: RuleResponse):
        self.assertTrue(all('has binary authorization disabled' in issue.evidence for issue in rule_result.issues))

    @rule_test('both_enabled_and_evmode_disabled', should_alert=False)
    def test_both_enabled_and_evmode_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('both_enabled_but_evmode_alwaysallow', should_alert=True)
    def test_both_enabled_but_evmode_alwaysallow(self, rule_result: RuleResponse):
        self.assertTrue(all('has binary authorization enabled but the evaluation mode set to always allow' in issue.evidence for issue in rule_result.issues))

    @rule_test('one_enabled', should_alert=True)
    def test_one_enabled(self, rule_result: RuleResponse):
        self.assertTrue(all('has binary authorization disabled' in issue.evidence for issue in rule_result.issues))
