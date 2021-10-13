from cloudrail.knowledge.rules.azure.non_context_aware.app_service_accessible_only_via_https_rule import AppServiceAccessibleOnlyViaHttpsRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceAccessibleOnlyViaHttpsRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceAccessibleOnlyViaHttpsRule()

    def test_https_only_set_to_true(self):
        self.run_test_case('https_only_set_to_true', should_alert=False)

    def test_https_only_set_to_false(self):
        self.run_test_case('https_only_set_to_false', should_alert=True)

    def test_https_only_is_missing(self):
        self.run_test_case('https_only_is_missing', should_alert=True)
