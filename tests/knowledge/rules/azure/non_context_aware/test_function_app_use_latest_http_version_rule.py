from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_http_version_rule import FunctionAppUseLatestHttpVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseLatestHttpVersionRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUseLatestHttpVersionRule()

    @parameterized.expand(
        [
            ["http2 enabled", True, False],
            ["http2 disabled", False, True]
        ]
    )
    def test_non_car_http_latest_in_function_app_fail(self, unused_name: str, http2_enable: bool, should_alert: bool):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.http2_enabled = http2_enable
        func_app.app_service_config = app_service_config
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
