from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_using_latest_version_rule import FunctionAppUsingLatestPythonVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseLatestPythonVersionRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUsingLatestPythonVersionRule()

    @parameterized.expand(
        [
            ['python version is 3.9 the rule should not alert', 'Python|3.9', False],
            ['python version is 3.10 the rule should not alert', 'Python|3.10', False],
            ['python version is 3.8 the rule should alert', 'Python|3.8', True],
            ['python version is empty the rule should not alert', '', False]
        ]
    )
    def test_non_car_function_app_using_latest_python_version_fail(self, unused_name: str, linux_fx_version: str, should_alert: bool):
        # Arrange
        function_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.linux_fx_version = linux_fx_version
        function_app.app_service_config = app_service_config
        function_app.name = 'my-func-app'
        function_app.with_aliases(function_app.name)
        context = AzureEnvironmentContext(function_apps=AliasesDict(*[function_app]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
