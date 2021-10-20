from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_public_access_rule import StorageAccountPublicAccessRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestStorageAccountPublicAccessRule(AzureBaseRuleTest):
    def get_rule(self):
        return StorageAccountPublicAccessRule()

    @rule_test('storage_account_public_access_disabled', False)
    def test_storage_account_secure_transfer_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_account_public_access_enabled', True)
    def test_storage_account_secure_transfer_enabled(self, rule_result: RuleResponse):
        pass
