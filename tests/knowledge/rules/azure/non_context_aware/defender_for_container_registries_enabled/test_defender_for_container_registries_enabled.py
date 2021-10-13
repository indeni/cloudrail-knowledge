from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import ContainerRegistriesDefenderEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestContainerRegistriesDefenderEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return ContainerRegistriesDefenderEnabledRule()

    def test_defender_for_container_registry_enabled(self):
        self.run_test_case('defender_for_container_registry_enabled', should_alert=False)

    def test_defender_for_container_registry_disabled(self):
        self.run_test_case('defender_for_container_registry_disabled', should_alert=True)
