import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_secure_transfer import StorageAccountSecureTransferRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from parameterized import parameterized


class TestStorageAccountSecureTransferRule(unittest.TestCase):
    def setUp(self):
        self.rule = StorageAccountSecureTransferRule()

    @parameterized.expand(
        [
            ['storage_account_secure_transfer_enabled',True, False],
            ['storage_account_secure_transfer_disabled', False, True],
        ]
    )
    def test_non_car_storage_account_default_network_access_denied(self, unused_name: str, enable_https_traffic_only: bool, should_alert: bool):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        storage_account.enable_https_traffic_only = enable_https_traffic_only
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
