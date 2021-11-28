from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_minimum_error_rule import PostgresLogMinimumErrorRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPostgresLogMinimumError(GcpBaseRuleTest):

    def get_rule(self):
        return PostgresLogMinimumErrorRule()

    @rule_test('log_min_error_off', should_alert=True)
    def test_log_min_error_off(self, rule_result: RuleResponse):
        pass

    @rule_test('log_min_error_on', should_alert=False)
    def test_log_min_error_on(self, rule_result: RuleResponse):
        pass

    @rule_test('log_min_error_not_defined', should_alert=False)
    def test_log_min_error_not_defined(self, rule_result: RuleResponse):
        pass
