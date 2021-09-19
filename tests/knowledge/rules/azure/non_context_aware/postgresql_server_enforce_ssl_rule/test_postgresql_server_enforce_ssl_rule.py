from cloudrail.knowledge.rules.azure.non_context_aware.postgresql_server_enforce_ssl_rule import PostgreSqlServerEnforceSslRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestPostgreSqlServerEnforceSslRule(AzureBaseRuleTest):
    def get_rule(self):
        return PostgreSqlServerEnforceSslRule()

    def test_postgresql_enforcing_ssl_enabled(self):
        self.run_test_case('postgresql_enforcing_ssl_enabled', False)

    def test_postgresql_enforcing_ssl_not_enabled(self):
        self.run_test_case('postgresql_enforcing_ssl_not_enabled', True)
