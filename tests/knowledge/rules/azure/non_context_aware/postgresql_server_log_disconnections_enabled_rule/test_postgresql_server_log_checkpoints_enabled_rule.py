from cloudrail.knowledge.rules.azure.non_context_aware.abstract_postgresql_servers_have_configuration_value_enabled_rule import \
    PostgresqlServersHaveLogCheckpointsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestPostgresqlServersHaveLogCheckpointsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return PostgresqlServersHaveLogCheckpointsEnabledRule()

    @rule_test('postgresql_log_disconnections_enabled', False)
    def test_postgresql_log_checkpoints_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('postgresql_log_disconnections_not_enabled', True)
    def test_postgresql_log_checkpoints_not_enabled(self, rule_result: RuleResponse):
        pass
