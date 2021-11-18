from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_cross_databases_ownership_chaining_rule import SqlCrossDatabasesOwnershipChainingRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestSqlCrossDatabasesOwnershipChainingOffRule(GcpBaseRuleTest):

    def get_rule(self):
        return SqlCrossDatabasesOwnershipChainingRule()

    @rule_test('cross_db_chaining_on', should_alert=True)
    def test_cross_db_chaining_on(self, rule_result: RuleResponse):
        pass

    @rule_test('cross_db_chaining_off', should_alert=False)
    def test_cross_db_chaining_off(self, rule_result: RuleResponse):
        pass
