from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import AppServicesDefenderEnabledRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServicesDefenderEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return AppServicesDefenderEnabledRule()

    @rule_test('defender_for_az_app_services_enabled', should_alert=False)
    def test_defender_for_app_services_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('defender_for_az_app_services_disabled', should_alert=True)
    def test_defender_for_app_services_disabled(self, rule_result: RuleResponse):
        pass
