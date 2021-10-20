from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.key_vault_purge_protection_enabled_rule import KeyVaultPurgeProtectionEnabledRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestKeyVaultPurgeProtectionEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KeyVaultPurgeProtectionEnabledRule()

    @rule_test('purge_protection_disabled_default', True)
    def test_purge_protection_disabled_default(self, rule_result: RuleResponse):
        pass

    @rule_test('purge_protection_enabled', False)
    def test_purge_protection_enabled(self, rule_result: RuleResponse):
        pass
