from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_Identity import Identity
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.rules.azure.non_context_aware.abstract_web_app_using_managed_identity_rule import \
    AppServiceUseManagedIdentityRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceUseManagedIdentityRule(TestCase):

    def setUp(self):
        self.rule = AppServiceUseManagedIdentityRule()

    @parameterized.expand(
        [
            ["app service not using a managed identity", None, True],
            ["app service using a managed identity", Identity('SystemAssigned', None), False]
        ]
    )
    def test_auth_states(self, unused_name: str, identity: Identity, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.identity = identity
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
