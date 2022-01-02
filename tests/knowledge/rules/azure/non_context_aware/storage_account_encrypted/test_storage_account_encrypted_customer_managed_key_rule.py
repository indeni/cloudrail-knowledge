from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_encrypted_customer_managed_key_rule import EnsureStorageAccountEncryptedCustomerManagedKeyRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureStorageAccountEncryptedCustomerManagedKeyRule(AzureBaseRuleTest):
    def get_rule(self):
        return EnsureStorageAccountEncryptedCustomerManagedKeyRule()

    @rule_test('storage_account_encrypted_enabled', should_alert=False)
    def test_storage_account_encrypted_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_account_encrypted_not_enabled', should_alert=True)
    def test_storage_account_encrypted_not_enabled(self, rule_result: RuleResponse):
        pass
