from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestJavaVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseLatestJavaVersionRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUsingLatestJavaVersionRule()

    @parameterized.expand(
        [
            ['java version linux is 11 the rule should alert', 'JAVA|11', None, False],
            ['java version win is 11 the rule should not alert', '', '11', False],
            ['java version linux is 1.8 the rule should alert', 'JAVA|8', '', True],
            ['java version win is 11 the rule should not alert', '', '1.8', True],
            ['java version win is 11 the rule should not alert', '', None, False],
            ['java version win is 11 the rule should not alert', '', '1.11', False],
            ['java version linux is 11 the rule should alert', 'PYTHON|11', None, False]
        ]
    )
    def test_non_car_function_app_using_latest_java_version(self, unused_name: str, linux_fx_version: str, java_version: str, should_alert: bool):
        # Arrange
        function_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        function_app_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        function_app_config.linux_fx_version = linux_fx_version
        function_app_config.java_version = java_version
        function_app.app_service_config = function_app_config
        context = AzureEnvironmentContext(function_apps=AliasesDict(function_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
