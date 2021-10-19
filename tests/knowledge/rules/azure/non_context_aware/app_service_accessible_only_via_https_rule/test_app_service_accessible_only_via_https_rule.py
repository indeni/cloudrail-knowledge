from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_accessible_only_via_https_rule import AppServiceAccessibleOnlyViaHttpsRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceAccessibleOnlyViaHttpsRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceAccessibleOnlyViaHttpsRule()

    @rule_test('https_only_set_to_true', should_alert=False)
    def test_https_only_set_to_true(self, rule_result: RuleResponse):
        pass

    @rule_test('https_only_set_to_false', should_alert=True)
    def test_https_only_set_to_false(self, rule_result: RuleResponse):
        pass

    @rule_test('https_only_is_missing', should_alert=True)
    def test_https_only_is_missing(self, rule_result: RuleResponse):
        pass
