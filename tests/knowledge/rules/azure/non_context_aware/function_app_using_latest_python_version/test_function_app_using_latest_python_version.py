from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestPythonVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppUseLatestPythonVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUsingLatestPythonVersionRule()

    @rule_test('python_is_not_latest', True)
    def test_function_app_no_linux_fx_version(self, rule_result: RuleResponse):
        pass

    @rule_test('python_is_latest', False)
    def test_function_app_python_is_latest_linux(self, rule_result: RuleResponse):
        pass
