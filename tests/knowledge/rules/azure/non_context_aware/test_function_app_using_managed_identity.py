from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_Identity import Identity
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.abstract_web_app_using_managed_identity_rule import \
     FunctionAppUseManagedIdentityRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseManagedIdentityRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUseManagedIdentityRule()

    @parameterized.expand(
        [
            ["function app not using a managed identity", None, True],
            ["function app using a managed identity", Identity('SystemAssigned', None), False]
        ]
    )
    def test_auth_states(self, unused_name: str, identity: Identity, should_alert: bool):
        # Arrange
        function_apps: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        function_apps.identity = identity
        function_apps.name = 'my-app-service'
        context = AzureEnvironmentContext(function_apps=AliasesDict(function_apps))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
