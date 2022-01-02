from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_log_disconnections_rule import PostgresLogDisconnectionsRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPostgresLogDisconnections(GcpBaseRuleTest):

    def get_rule(self):
        return PostgresLogDisconnectionsRule()

    @rule_test('postgres_log_disconnections_off', should_alert=True)
    def test_postgres_log_disconnections_off(self, rule_result: RuleResponse):
        pass

    @rule_test('postgres_log_disconnections_on', should_alert=False)
    def test_postgres_log_disconnections_on(self, rule_result: RuleResponse):
        pass
