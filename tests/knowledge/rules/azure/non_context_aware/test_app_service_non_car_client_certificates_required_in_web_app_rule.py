import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_client_certificates_required_in_web_app_rule import \
    AppServiceClientCertificatesRequiredRule
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAppServiceClientCertificatesRequiredRule(unittest.TestCase):
    def setUp(self):
        self.rule = AppServiceClientCertificatesRequiredRule()

    @parameterized.expand(
        [
            ["Client certificates is enabled", True, False],
            ["Client certificates is not enabled", False, True]
        ]
    )
    def test_states(self, unused_name: str, client_cert_required: bool, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service.client_cert_required = client_cert_required
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
