import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.security.azure_security_center_contact import AzureSecurityCenterContact
from cloudrail.knowledge.rules.azure.non_context_aware.email_notification_high_severity_alerts_enabled_rule import \
    EmailNotificationHighSeverityAlertsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEmailNotificationHighSeverityAlertsEnabled(unittest.TestCase):
    def setUp(self):
        self.rule = EmailNotificationHighSeverityAlertsEnabledRule()

    @parameterized.expand(
        [
            ['Alert Notification True - Ok', True, False],
            ['Alert Notification False - Should Alert', False, True]
        ]
    )
    def test_alert_notifications(self, unused_name: str, alert_notifications: bool, should_alert: bool):
        # Arrange
        sc_contact = create_empty_entity(AzureSecurityCenterContact)
        sc_contact.alert_notifications = alert_notifications
        context = AzureEnvironmentContext(security_center_contacts=AliasesDict(sc_contact))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
