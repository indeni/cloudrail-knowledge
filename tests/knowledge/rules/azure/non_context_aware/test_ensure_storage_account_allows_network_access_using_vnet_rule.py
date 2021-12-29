from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_allows_network_access_using_vnet_rule import EnsureStorageAccountAllowsNetworkAccessUsingVnetRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureStorageAccountAllowsNetworkAccessUsingVnetRule(TestCase):
    def setUp(self):
        self.rule = EnsureStorageAccountAllowsNetworkAccessUsingVnetRule()

    @parameterized.expand(
        [
            ["Ip rules only", {"ip_rules": ["1.2.3.4"], "virtual_network_subnet_ids": []}, 1, RuleResultType.FAILED],
            ["Virtual network subnet ids only", {"ip_rules": [], "virtual_network_subnet_ids": ["azurerm_subnet.snet.id"]}, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_ensure_storage_account_allows_network_access_using_vnet_rule(self, unused_name: str, data_dict: dict, total_issues: int, rule_status: RuleResultType):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        storage_account.network_rules = create_empty_entity(AzureStorageAccountNetworkRules)
        storage_account.network_rules.ip_rules = data_dict["ip_rules"]
        storage_account.network_rules.virtual_network_subnet_ids = data_dict["virtual_network_subnet_ids"]

        context = AzureEnvironmentContext(storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
