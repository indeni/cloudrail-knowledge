from cloudrail.knowledge.rules.azure.non_context_aware.app_service_authentication_enable_rule import AppServiceAuthenticationEnableRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceAuthenticationEnableRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceAuthenticationEnableRule()

    def test_auth_enable(self):
        self.run_test_case('auth_enable', should_alert=False)

    def test_auth_disable(self):
        self.run_test_case('auth_disable', should_alert=True)

    def test_auth_missing(self):
        self.run_test_case('auth_missing', should_alert=True)
