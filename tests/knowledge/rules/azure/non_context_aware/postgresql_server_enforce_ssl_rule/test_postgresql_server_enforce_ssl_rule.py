from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.postgresql_server_enforce_ssl_rule import PostgreSqlServerEnforceSslRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestPostgreSqlServerEnforceSslRule(AzureBaseRuleTest):
    def get_rule(self):
        return PostgreSqlServerEnforceSslRule()

    @rule_test('postgresql_enforcing_ssl_enabled', False)
    def test_postgresql_enforcing_ssl_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('postgresql_enforcing_ssl_not_enabled', True)
    def test_postgresql_enforcing_ssl_not_enabled(self, rule_result: RuleResponse):
        pass
