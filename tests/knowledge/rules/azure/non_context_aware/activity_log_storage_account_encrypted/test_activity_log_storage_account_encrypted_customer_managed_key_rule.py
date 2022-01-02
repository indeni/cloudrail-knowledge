from cloudrail.knowledge.rules.azure.non_context_aware.ensure_activity_log_storage_account_encrypted_customer_managed_key_rule import EnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule(AzureBaseRuleTest):
    def get_rule(self):
        return EnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule()

    @rule_test('activity_log_storage_account_encrypted_enabled', should_alert=False)
    def test_storage_account_encrypted_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('activity_log_storage_account_encrypted_not_enabled', should_alert=True)
    def test_storage_account_encrypted_not_enabled(self, rule_result: RuleResponse):
        pass
