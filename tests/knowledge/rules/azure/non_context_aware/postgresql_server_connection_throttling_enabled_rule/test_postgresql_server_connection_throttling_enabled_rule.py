from cloudrail.knowledge.rules.azure.non_context_aware.abstract_postgresql_servers_have_configuration_value_enabled_rule import \
    PostgresqlServersHaveConnectionThrottlingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestPostgresqlServersHaveConnectionThrottlingEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return PostgresqlServersHaveConnectionThrottlingEnabledRule()

    @rule_test('postgresql_throttling_enabled', False)
    def test_postgresql_throttling_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('postgresql_throttling_not_enabled', True)
    def test_postgresql_throttling_not_enabled(self, rule_result: RuleResponse):
        pass
