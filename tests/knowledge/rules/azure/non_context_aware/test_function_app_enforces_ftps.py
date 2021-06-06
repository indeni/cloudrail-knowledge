from unittest import TestCase

from cloudrail.knowledge.context.aliases_dict import AliasesDict

from cloudrail.knowledge.rules.base_rule import RuleResultType

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from cloudrail.knowledge.context.azure.webapp.azure_app_service import SiteConfig, FtpState, AzureAppService
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule


class TestFunctionAppEnforcesFtps(TestCase):

    def setUp(self):
        self.rule = FunctionAppEnforcesFtpsOnlyRule()

    def test_ftps_enabled(self):
        # Arrange
        site_config: SiteConfig = SiteConfig(FtpState.FTPS_ONLY)
        app: AzureAppService = create_empty_entity(AzureAppService)
        app.site_config = site_config
        app.name = 'my-app'
        context = AzureEnvironmentContext(app_services=AliasesDict(app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_ftps_disabled(self):
        # Arrange
        app: AzureAppService = create_empty_entity(AzureAppService)
        app.name = 'my-app'
        context = AzureEnvironmentContext(app_services=AliasesDict(app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
