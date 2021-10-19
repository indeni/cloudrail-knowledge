from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_authentication_enable_rule import FunctionAppAuthenticationEnableRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppAuthenticationEnable(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppAuthenticationEnableRule()

    @rule_test('auth_enable', should_alert=False)
    def test_auth_enable(self, rule_result: RuleResponse):
        pass

    @rule_test('auth_disable', should_alert=True)
    def test_auth_disable(self, rule_result: RuleResponse):
        pass
