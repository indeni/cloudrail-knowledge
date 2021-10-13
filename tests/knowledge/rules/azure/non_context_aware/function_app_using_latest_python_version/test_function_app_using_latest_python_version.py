from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_python_version_rule import \
    FunctionAppUseLatestPythonVersionRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppUseLatestPythonVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseLatestPythonVersionRule()

    def test_function_app_no_linux_fx_version(self):
        self.run_test_case('python_is_not_latest', True)

    def test_function_app_python_is_latest_linux(self):
        self.run_test_case('python_is_latest', False)
