from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_secure_transfer import StorageAccountSecureTransferRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestStorageAccountSecureTransferRule(AzureBaseRuleTest):
    def get_rule(self):
        return StorageAccountSecureTransferRule()

    @rule_test('storage_account_secure_transfer_disabled', True)
    def test_storage_account_secure_transfer_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_account_secure_transfer_enabled', False)
    def test_storage_account_secure_transfer_enabled(self, rule_result: RuleResponse):
        pass
