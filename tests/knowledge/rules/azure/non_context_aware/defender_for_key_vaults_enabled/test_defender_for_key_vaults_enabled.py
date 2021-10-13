from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import KeyVaultsDefenderEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestKeyVaultsDefenderEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return KeyVaultsDefenderEnabledRule()

    def test_defender_for_container_registry_enabled(self):
        self.run_test_case('defender_for_key_vaults_enabled', should_alert=False)

    def test_defender_for_container_registry_disabled(self):
        self.run_test_case('defender_for_key_vaults_disabled', should_alert=True)
