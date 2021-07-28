from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_accessible_only_via_https_rule import AppServiceAccessibleOnlyViaHttpsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceAccessibleOnlyViaHttpsRule(TestCase):

    def setUp(self):
        self.rule = AppServiceAccessibleOnlyViaHttpsRule()

    @parameterized.expand(
        [
            ["https_only enable", True, False],
            ["https_only disable", False, True]
        ]
    )
    def test_auth_states(self, unused_name: str, https_only: bool, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.https_only = https_only
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
