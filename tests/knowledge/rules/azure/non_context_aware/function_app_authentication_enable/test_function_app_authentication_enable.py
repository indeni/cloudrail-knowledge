from cloudrail.knowledge.rules.azure.non_context_aware.function_app_authentication_enable_rule import FunctionAppAuthenticationEnableRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppAuthenticationEnable(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppAuthenticationEnableRule()

    def test_auth_enable(self):
        self.run_test_case('auth_enable',
                           should_alert=False)

    def test_auth_disable(self):
        self.run_test_case('auth_disable',
                           should_alert=True)
