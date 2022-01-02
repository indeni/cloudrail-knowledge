from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_log_min_duration_disable_rule import SqlLogMinimumDurationDisableRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPostgresLogMinDuration(GcpBaseRuleTest):

    def get_rule(self):
        return SqlLogMinimumDurationDisableRule()

    @rule_test('log_min_duration_off', should_alert=False)
    def test_log_min_duration_off(self, rule_result: RuleResponse):
        pass

    @rule_test('log_min_duration_on', should_alert=True)
    def test_log_min_duration_on(self, rule_result: RuleResponse):
        pass
