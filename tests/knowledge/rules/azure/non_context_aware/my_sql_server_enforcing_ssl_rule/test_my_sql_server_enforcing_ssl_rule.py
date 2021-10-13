from cloudrail.knowledge.rules.azure.non_context_aware.my_sql_server_enforcing_ssl_rule import MySqlServerEnforcingSslRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestMySqlServerEnforcingSslRule(AzureBaseRuleTest):
    def get_rule(self):
        return MySqlServerEnforcingSslRule()

    def test_mysql_enforcing_ssl_enabled(self):
        self.run_test_case('mysql_enforcing_ssl_enabled', False)

    def test_mysql_enforcing_ssl_not_enabled(self):
        self.run_test_case('mysql_enforcing_ssl_not_enabled', True)
