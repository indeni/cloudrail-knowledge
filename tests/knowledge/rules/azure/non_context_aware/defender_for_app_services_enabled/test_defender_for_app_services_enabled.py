from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import AppServicesDefenderEnabledRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServicesDefenderEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return AppServicesDefenderEnabledRule()

    def test_defender_for_app_services_enabled(self):
        self.run_test_case('defender_for_az_app_services_enabled', should_alert=False)

    def test_defender_for_app_services_disabled(self):
        self.run_test_case('defender_for_az_app_services_disabled', should_alert=True)
