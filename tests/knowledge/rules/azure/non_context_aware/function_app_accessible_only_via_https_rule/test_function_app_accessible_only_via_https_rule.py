from cloudrail.knowledge.rules.azure.non_context_aware.function_app_accessible_only_via_https_rule import FunctionAppAccessibleOnlyViaHttpsRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppAccessibleOnlyViaHttpsRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppAccessibleOnlyViaHttpsRule()

    def test_https_only_set_to_true(self):
        self.run_test_case('https_only_set_to_true', should_alert=False)

    def test_https_only_set_to_false(self):
        self.run_test_case('https_only_set_to_false', should_alert=True)

    def test_https_only_is_missing(self):
        self.run_test_case('https_only_is_missing', should_alert=True)
