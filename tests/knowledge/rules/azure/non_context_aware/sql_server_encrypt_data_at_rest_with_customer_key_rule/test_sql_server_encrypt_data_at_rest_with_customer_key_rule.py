from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.sql_server_encrypt_data_at_rest_with_customer_key_rule import \
    SqlServerEncryptDataAtRestWithCustomerKeyRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestSqlServerEncryptDataAtRestWithCustomerKeyRule(AzureBaseRuleTest):
    def get_rule(self):
        return SqlServerEncryptDataAtRestWithCustomerKeyRule()

    @rule_test('sql_encryption_customer_key_not_set', True)
    def test_sql_encryption_customer_key_not_set(self, rule_result: RuleResponse):
        pass

    @rule_test('sql_encryption_customer_key_set', False)
    def test_sql_encryption_customer_key_set(self, rule_result: RuleResponse):
        pass
