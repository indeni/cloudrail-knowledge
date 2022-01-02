from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestPythonVersionRule, \
    AppServiceUsingLatestPhpVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceUseLatestPhpVersionRule(AzureBaseRuleTest):

    def get_rule(self):
        return AppServiceUsingLatestPhpVersionRule()

    @rule_test('latest_php_version', False)
    def test_function_app_latest_php_version(self, rule_result: RuleResponse):
        pass

    @rule_test('not_latest_php_version', True)
    def test_function_app_not_latest_java_version(self, rule_result: RuleResponse):
        pass
