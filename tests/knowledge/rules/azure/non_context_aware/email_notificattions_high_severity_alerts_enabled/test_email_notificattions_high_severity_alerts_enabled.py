from cloudrail.knowledge.rules.azure.non_context_aware.email_notification_high_severity_alerts_enabled_rule import \
    EmailNotificationHighSeverityAlertsEnabledRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppAuthenticationEnable(AzureBaseRuleTest):

    def get_rule(self):
        return EmailNotificationHighSeverityAlertsEnabledRule()

    def test_email_notification_on(self):
        self.run_test_case('email_notification_on', should_alert=False)

    def test_email_notification_off(self):
        self.run_test_case('email_notification_off', should_alert=True)
