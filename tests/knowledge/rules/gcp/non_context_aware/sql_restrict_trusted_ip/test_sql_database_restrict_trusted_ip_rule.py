from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_restrict_trusted_ip_rule import \
    SqlDatabaseRestrictTrustedIpRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestSqlDatabaseRestrictTrustedIpRule(GcpBaseRuleTest):
    def get_rule(self):
        return SqlDatabaseRestrictTrustedIpRule()

    @rule_test('cloudsql_not_open', should_alert=False)
    def test_restrict_trusted_ip_not_open(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudsql_open', should_alert=True)
    def test_restrict_trusted_ip_open(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudsql_private_and_open', should_alert=True)
    def test_restrict_trusted_ip_private_and_open(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudsql_private_ip', should_alert=False)
    def test_restrict_trusted_ip_private(self, rule_result: RuleResponse):
        pass
