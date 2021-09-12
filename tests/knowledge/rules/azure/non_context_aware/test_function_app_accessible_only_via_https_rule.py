from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_accessible_only_via_https_rule import FunctionAppAccessibleOnlyViaHttpsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppAccessibleOnlyViaHttpsRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppAccessibleOnlyViaHttpsRule()

    @parameterized.expand(
        [
            ["https_only enable", True, False],
            ["https_only disable", False, True]
        ]
    )
    def test_auth_states(self, unused_name: str, https_only: bool, should_alert: bool):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.https_only = https_only
        func_app.name = 'my-func-app'
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
