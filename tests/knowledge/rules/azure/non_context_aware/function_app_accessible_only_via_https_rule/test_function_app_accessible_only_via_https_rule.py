from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_accessible_only_via_https_rule import FunctionAppAccessibleOnlyViaHttpsRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppAccessibleOnlyViaHttpsRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppAccessibleOnlyViaHttpsRule()

    @rule_test('https_only_set_to_true', should_alert=False)
    def test_https_only_set_to_true(self, rule_result: RuleResponse):
        pass

    @rule_test('https_only_set_to_false', should_alert=True)
    def test_https_only_set_to_false(self, rule_result: RuleResponse):
        pass

    @rule_test('https_only_is_missing', should_alert=True)
    def test_https_only_is_missing(self, rule_result: RuleResponse):
        pass
