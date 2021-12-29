from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_use_http_version_rule import AppServiceUseLatestHttpVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceLatestHttpVersionRule(TestCase):

    def setUp(self):
        self.rule = AppServiceUseLatestHttpVersionRule()

    @parameterized.expand(
        [
            ["http2 enabled", True, False],
            ["http2 disabled", False, True]
        ]
    )
    def test_app_service_http_latest_version(self, unused_name: str, http2_enable: bool, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.http2_enabled = http2_enable
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
