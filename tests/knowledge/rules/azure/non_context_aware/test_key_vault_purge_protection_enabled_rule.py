from unittest import TestCase

from cloudrail.knowledge.context.azure.resources.keyvault.azure_key_vault import AzureKeyVault
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.key_vault_purge_protection_enabled_rule import KeyVaultPurgeProtectionEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from parameterized import parameterized


class TestKeyVaultPurgeProtectionEnabledRule(TestCase):

    def setUp(self):
        self.rule = KeyVaultPurgeProtectionEnabledRule()

    @parameterized.expand(
        [
            ['purge_protection_enabled', True, False],
            ['purge_protection_enabled', False, True],
        ]
    )
    def test_non_car_key_vault_purge_protection_enabled(self, unused_name: str, purge_enabled: bool, should_alert: bool):
        # Arrange
        key_vault: AzureKeyVault = create_empty_entity(AzureKeyVault)
        key_vault.name = 'tmp-name'
        key_vault.purge_protection_enabled = purge_enabled
        context = AzureEnvironmentContext(key_vaults=AliasesDict(key_vault))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
