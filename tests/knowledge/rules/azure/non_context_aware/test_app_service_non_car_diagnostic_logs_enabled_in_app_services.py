import unittest
from typing import Optional

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.security.azure_security_center_subscription_pricing import AzureSecurityCenterSubscriptionPricing, \
    SubscriptionPricingResourceType, SubscriptionPricingTier
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.webapp.diagnostic_logs import DiagnosticLogs
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_diagnostic_logs_enabled_in_app_services_rule import \
    AppServiceDiagnosticLogsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.azure.non_context_aware.azure_defender_enabled_rules import NonCarAzureKubernetesDefenderEnabled


class TestAppServiceDiagnosticLogsRule(unittest.TestCase):
    def setUp(self):
        self.rule = AppServiceDiagnosticLogsRule()

    @parameterized.expand(
        [
            ['Only detailed error logging disabled ', DiagnosticLogs(False, True, True), True, "The web app `test_alert_notifications` does not have detailed error logging enabled"],
            ['Only http logging disabled',  DiagnosticLogs(True, False, True), True, "The web app `test_alert_notifications` does not have HTTP logging enabled"],
            ['Only request tracing disabled', DiagnosticLogs(True, True, False), True, "The web app `test_alert_notifications` does not have request tracing enabled"],
            ['All disabled', DiagnosticLogs(False, False, False), True, "The web app `test_alert_notifications` does not have HTTP logging enabled. The web app `test_alert_notifications` does not have request tracing enabled. The web app `test_alert_notifications` does not have detailed error logging enabled"],
            ['All enabled', DiagnosticLogs(True, True, True), False, None],
            ['logs are None', None, True, "The web app `test_alert_notifications` does not have logging enabled"]
        ]
    )
    def test_alert_notifications(self, unused_name: str, logs: DiagnosticLogs, should_alert: bool, evidence_string: Optional[str]):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'test_alert_notifications'
        app_service_config: AzureAppServiceConfig = create_empty_entity(AzureAppServiceConfig)
        app_service_config.logs = logs
        app_service.app_service_config = app_service_config
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))

        # Act
        result = self.rule.run(context, {})

        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
            self.assertEqual(evidence_string, result.issues[0].evidence)
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
