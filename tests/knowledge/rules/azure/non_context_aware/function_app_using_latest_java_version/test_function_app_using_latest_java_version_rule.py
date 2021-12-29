from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestJavaVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppUsingLatestJavaVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUsingLatestJavaVersionRule()

    @rule_test('functionapp_lin_java_is_latest', False)
    def test_functionapp_java_isnot_latest_linux(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_lin_java_isnot_latest', True)
    def test_functionapp_java_latest_linux(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_win_java_is_latest', False)
    def test_functionapp_java_isnot_latest_win(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_win_java_isnot_latest', True)
    def test_functionapp_java_latest_win(self, rule_result: RuleResponse):
        pass
