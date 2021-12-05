from cloudrail.knowledge.rules.azure.non_context_aware.function_app_using_managed_identity_rule import \
    FunctionAppUseManagedIdentityRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppUseManagedIdentityRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseManagedIdentityRule()

    @rule_test('not_use_managed_identity', True)
    def test_function_app_not_use_managed_identity(self, rule_result: RuleResponse):
        pass

    @rule_test('use_user_assigned', False)
    def test_function_app_use_user_assigned(self, rule_result: RuleResponse):
        pass

    @rule_test('use_system_assigned', False)
    def test_function_app_use_system_assigned(self, rule_result: RuleResponse):
        pass
