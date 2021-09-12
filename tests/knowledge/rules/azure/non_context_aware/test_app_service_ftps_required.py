import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_ftps_required_rule import AppServiceFtpsRequiredRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestAppServiceFtpsRequired(unittest.TestCase):
    def setUp(self):
        self.rule = AppServiceFtpsRequiredRule()

    @parameterized.expand(
        [
            ["FTPS status all allow should alert", FtpsState.ALL_ALLOWED, True],
            ["FTPS status disable should not alert", FtpsState.DISABLED, False],
            ["FTPS status is secured should not alert", FtpsState.FTPS_ONLY, False]
        ]
    )
    def test_states(self, unused_name: str, ftps_state: FtpsState, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.ftps_state = ftps_state
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

    def test_settings_not_exist(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
