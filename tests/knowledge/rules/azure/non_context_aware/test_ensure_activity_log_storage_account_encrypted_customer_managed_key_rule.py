import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_customer_managed_key import AzureStorageAccountCustomerManagedKey
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_activity_log_storage_account_encrypted_customer_managed_key_rule import EnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from parameterized import parameterized


class TestEnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule()

    @parameterized.expand(
        [
            ['Activity log storage account encrypted enabled', True, 0, RuleResultType.SUCCESS],
            ['Activity log storage account encrypted not_enabled', False, 1, RuleResultType.FAILED],
        ]
    )
    def test_activity_log_storage_account_encrypted_with_byok(self, unused_name: str, is_encrypted: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        monitor_diagnostic_setting: AzureMonitorDiagnosticSetting = create_empty_entity(AzureMonitorDiagnosticSetting)
        monitor_diagnostic_setting.name = 'Monitor diagnostic setting'
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        storage_account.storage_name = 'Storage account'
        storage_account.storage_account_customer_managed_key = create_empty_entity(AzureStorageAccountCustomerManagedKey) if is_encrypted else None
        monitor_diagnostic_setting.storage_account = storage_account
        context = AzureEnvironmentContext(monitor_diagnostic_settings=AliasesDict(monitor_diagnostic_setting), storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
