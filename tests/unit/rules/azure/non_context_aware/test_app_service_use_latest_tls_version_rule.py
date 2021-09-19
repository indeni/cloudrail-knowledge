from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_use_latest_tls_version_rule import AppServiceUseLatestTlsVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceUseLatestTlsVersionRule(TestCase):

    def setUp(self):
        self.rule = AppServiceUseLatestTlsVersionRule()

    @parameterized.expand(
        [
            ['tls version is 1.1 the rule should alert', '1.1', True],
            ['tls version is 1.2 the rule should not alert', '1.2', False],
            ['tls version is 1.4 the rule should not alert', '1.4', False]
        ]
    )
    def test_non_car_app_service_using_latest_tls_version(self, unused_name: str, tls_version: str, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.minimum_tls_version = tls_version
        app_service.app_service_config = app_service_config
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
