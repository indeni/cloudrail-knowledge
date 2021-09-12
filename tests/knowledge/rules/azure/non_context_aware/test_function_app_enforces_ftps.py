from unittest import TestCase

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule


class TestFunctionAppEnforcesFtps(TestCase):

    def setUp(self):
        self.rule = FunctionAppEnforcesFtpsOnlyRule()

    @parameterized.expand(
        [
            ["FTPS status all allow should alert", FtpsState.ALL_ALLOWED, True],
            ["FTPS status disable should not alert", FtpsState.DISABLED, False],
            ["FTPS status is secured should not alert", FtpsState.FTPS_ONLY, False]
        ]
    )
    def test_ftps_enabled(self, unused_name: str, ftps_state: FtpsState, should_alert: bool):
        # Arrange
        app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.ftps_state = ftps_state
        app.app_service_config = app_service_config

        context = AzureEnvironmentContext(function_apps=AliasesDict(app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_settings_not_exist(self):
        # Arrange
        app_service: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        context = AzureEnvironmentContext(function_apps=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
