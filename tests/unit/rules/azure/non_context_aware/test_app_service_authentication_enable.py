from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_authentication_enable_rule import AppServiceAuthenticationEnableRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceAuthenticationEnable(TestCase):

    def setUp(self):
        self.rule = AppServiceAuthenticationEnableRule()

    @parameterized.expand(
        [
            ["auth enabled should not alert", True, False],
            ["auth disabled should alert", False, True]
        ]
    )
    def test_auth_states(self, unused_name: str, auth_enable: bool, should_alert: bool):
        # Arrange
        auth_settings: AuthSettings = AuthSettings(auth_enable)
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.auth_settings = auth_settings
        app_service.app_service_config = app_service_config
        app_service.name = 'my-app-service'
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))

    def test_settings_not_exist(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_auth_settings_not_exist(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.auth_settings = None
        app_service.app_service_config = app_service_config
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
