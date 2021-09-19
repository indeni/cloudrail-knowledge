
import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules, BypassTrafficType
from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_allow_network_access_trusted_azure_services_rule import \
    StorageAccountAllowNetworkAccessTrustedAzureResourcesRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from parameterized import parameterized


class TestStorageAccountAllowNetworkAccessTrustedAzureResourcesRule(unittest.TestCase):
    def setUp(self):
        self.rule = StorageAccountAllowNetworkAccessTrustedAzureResourcesRule()

    @parameterized.expand(
        [
            ['storage_account_allow_azure_trusted_access', [BypassTrafficType.AZURESERVICES, BypassTrafficType.METRICS], False],
            ['storage_account_do_not_allow_azure_trusted_access', [BypassTrafficType.METRICS], True],
        ]
    )
    def test_non_car_storage_account_network_access_trusted_azure_services(self, unused_name: str, bypass_traffic: list, should_alert: bool):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        network_rule: AzureStorageAccountNetworkRules = create_empty_entity(AzureStorageAccountNetworkRules)
        network_rule.bypass_traffic = bypass_traffic
        storage_account.network_rules = network_rule
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
