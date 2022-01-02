import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_customer_managed_key import AzureStorageAccountCustomerManagedKey
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_encrypted_customer_managed_key_rule import EnsureStorageAccountEncryptedCustomerManagedKeyRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from parameterized import parameterized


class TestEnsureStorageAccountEncryptedCustomerManagedKeyRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureStorageAccountEncryptedCustomerManagedKeyRule()

    @parameterized.expand(
        [
            ['Storage account encrypted enabled', True, 0, RuleResultType.SUCCESS],
            ['Storage account encrypted not_enabled', False, 1, RuleResultType.FAILED],
        ]
    )
    def test_storage_account_encrypted_customer_managed_key(self, unused_name: str, is_encrypted: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        storage_account.storage_account_customer_managed_key = create_empty_entity(AzureStorageAccountCustomerManagedKey) if is_encrypted else None
        storage_account.storage_name = 'storage_account'
        context = AzureEnvironmentContext(storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
