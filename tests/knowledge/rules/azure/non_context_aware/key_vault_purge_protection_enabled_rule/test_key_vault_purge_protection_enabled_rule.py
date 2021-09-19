from cloudrail.knowledge.rules.azure.non_context_aware.key_vault_purge_protection_enabled_rule import KeyVaultPurgeProtectionEnabledRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestKeyVaultPurgeProtectionEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KeyVaultPurgeProtectionEnabledRule()

    def test_purge_protection_disabled_default(self):
        self.run_test_case('purge_protection_disabled_default', True)

    def test_purge_protection_enabled(self):
        self.run_test_case('purge_protection_enabled', False)
