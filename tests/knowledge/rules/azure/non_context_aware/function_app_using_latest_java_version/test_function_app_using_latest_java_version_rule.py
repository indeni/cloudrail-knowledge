from cloudrail.knowledge.rules.azure.non_context_aware.function_app_non_car_function_app_using_latest_java_version_rule import \
    FunctionAppUsingLatestJavaVersionRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppUsingLatestJavaVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUsingLatestJavaVersionRule()

    def test_functionapp_java_isnot_latest_linux(self):
        self.run_test_case('functionapp_lin_java_is_latest', False)

    def test_functionapp_java_latest_linux(self):
        self.run_test_case('functionapp_lin_java_isnot_latest', True)

    def test_functionapp_java_isnot_latest_win(self):
        self.run_test_case('functionapp_win_java_is_latest', False)

    def test_functionapp_java_latest_win(self):
        self.run_test_case('functionapp_win_java_isnot_latest', True)
