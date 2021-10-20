from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_no_public_ip_rule import \
    SqlDatabaseNoPublicIpRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestSqlDatabaseNoPublicIpRule(GcpBaseRuleTest):
    def get_rule(self):
        return SqlDatabaseNoPublicIpRule()

    @rule_test('both_public', should_alert=True, number_of_issue_items=2)
    def test_ssl_required_false(self, rule_result: RuleResponse):
        pass

    @rule_test('no_public', should_alert=False)
    def test_ssl_required_true(self, rule_result: RuleResponse):
        pass

    @rule_test('one_public', should_alert=True)
    def test_ssl_required_not_specified(self, rule_result: RuleResponse):
        pass