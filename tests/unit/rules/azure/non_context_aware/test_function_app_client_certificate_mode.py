from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_client_certificate_mode_rule import FunctionAppClientCertificateModeRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppClientCertificateMode(TestCase):

    def setUp(self):
        self.rule = FunctionAppClientCertificateModeRule()

    def test_client_cert_required(self):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.client_cert_mode = FieldMode.REQUIRED
        func_app.name = 'my-func-app'
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_client_cert_optional(self):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.client_cert_mode = FieldMode.OPTIONAL
        func_app.name = 'my-func-app'
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
