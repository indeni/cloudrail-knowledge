from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.my_sql_server_enforcing_ssl_rule import MySqlServerEnforcingSslRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestMySqlServerEnforcingSslRule(AzureBaseRuleTest):
    def get_rule(self):
        return MySqlServerEnforcingSslRule()

    @rule_test('mysql_enforcing_ssl_enabled', False)
    def test_mysql_enforcing_ssl_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('mysql_enforcing_ssl_not_enabled', True)
    def test_mysql_enforcing_ssl_not_enabled(self, rule_result: RuleResponse):
        pass
