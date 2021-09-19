from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_public_access_rule import StorageAccountPublicAccessRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestStorageAccountPublicAccessRule(AzureBaseRuleTest):
    def get_rule(self):
        return StorageAccountPublicAccessRule()

    def test_storage_account_secure_transfer_disabled(self):
        self.run_test_case('storage_account_public_access_disabled', False)

    def test_storage_account_secure_transfer_enabled(self):
        self.run_test_case('storage_account_public_access_enabled', True)
