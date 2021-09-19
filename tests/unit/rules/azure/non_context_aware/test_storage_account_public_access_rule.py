import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_public_access_rule import StorageAccountPublicAccessRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from parameterized import parameterized


class TestStorageAccountPublicAccessRule(unittest.TestCase):
    def setUp(self):
        self.rule = StorageAccountPublicAccessRule()

    @parameterized.expand(
        [
            ['storage_account_public_access_disabled', False, False],
            ['storage_account_public_access_enabled', True, True],
        ]
    )
    def test_non_car_storage_account_public_access(self, unused_name: str, allow_public_access: bool, should_alert: bool):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        storage_account.allow_blob_public_access = allow_public_access
        storage_account.storage_name = 'storage_account'
        context = AzureEnvironmentContext(storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
