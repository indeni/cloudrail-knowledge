from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_lock_waits_on_rule import PostgresLogLockWaitsOnRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPostgresLogLockWaits(GcpBaseRuleTest):

    def get_rule(self):
        return PostgresLogLockWaitsOnRule()

    @rule_test('postgres_log_lock_waits_off', should_alert=True)
    def test_postgres_log_lock_waits_on(self, rule_result: RuleResponse):
        pass

    @rule_test('postgres_log_lock_waits_on', should_alert=False)
    def test_postgres_log_lock_waits_off(self, rule_result: RuleResponse):
        pass
