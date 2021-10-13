from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_secure_transfer import StorageAccountSecureTransferRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestStorageAccountSecureTransferRule(AzureBaseRuleTest):
    def get_rule(self):
        return StorageAccountSecureTransferRule()

    def test_storage_account_secure_transfer_disabled(self):
        self.run_test_case('storage_account_secure_transfer_disabled', True)

    def test_storage_account_secure_transfer_enabled(self):
        self.run_test_case('storage_account_secure_transfer_enabled', False)
