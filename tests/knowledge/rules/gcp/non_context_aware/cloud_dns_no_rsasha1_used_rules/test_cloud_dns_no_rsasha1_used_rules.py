from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.cloud_dns_no_rsasha1_used_rules import CloudDnsNoRsasha1UsedRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestCloudDnsNoRsasha1UsedRule(GcpBaseRuleTest):
    def get_rule(self):
        return CloudDnsNoRsasha1UsedRule()

    @rule_test('rsasha1_in_use', should_alert=True)
    def test_rsasha1_in_use(self, rule_result: RuleResponse):
        pass

    @rule_test('rsasha1_not_in_use', should_alert=False)
    def test_rsasha1_not_in_use(self, rule_result: RuleResponse):
        pass
