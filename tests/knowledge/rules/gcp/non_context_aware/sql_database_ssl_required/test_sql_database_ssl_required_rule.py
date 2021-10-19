from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_ssl_required_rule import SqlDatabaseSslRequiredRule

from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestSqlDatabaseSslRequiredRule(GcpBaseRuleTest):
    def get_rule(self):
        return SqlDatabaseSslRequiredRule()

    ### always_use_cache_on_jenkins=True will be removed with CR-2612

    @rule_test('ssl_required_false', should_alert=True)
    def test_ssl_required_false(self, rule_result: RuleResponse):
        pass

    @rule_test('ssl_required_true', should_alert=False)
    def test_ssl_required_true(self, rule_result: RuleResponse):
        pass

    @rule_test('ssl_required_not_specified', should_alert=True)
    def test_ssl_required_not_specified(self, rule_result: RuleResponse):
        pass
