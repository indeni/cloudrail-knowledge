from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestPythonVersionRule, \
    AppServiceUsingLatestJavaVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceUseLatestJavaVersionRule(AzureBaseRuleTest):

    def get_rule(self):
        return AppServiceUsingLatestJavaVersionRule()

    @rule_test('latest_java_version', False)
    def test_function_app_latest_java_version(self, rule_result: RuleResponse):
        pass

    @rule_test('not_latest_java_version', True)
    def test_function_app_not_latest_java_version(self, rule_result: RuleResponse):
        pass

    @rule_test('not_latest_container_java_version', True)
    def test_function_app_not_latest_container_java_version(self, rule_result: RuleResponse):
        pass

    @rule_test('latest_container_java_version', False)
    def test_function_app_latest_container_java_version(self, rule_result: RuleResponse):
        pass
