from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.email_notification_high_severity_alerts_enabled_rule import \
    EmailNotificationHighSeverityAlertsEnabledRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppAuthenticationEnable(AzureBaseRuleTest):

    def get_rule(self):
        return EmailNotificationHighSeverityAlertsEnabledRule()

    @rule_test('email_notification_on', should_alert=False)
    def test_email_notification_on(self, rule_result: RuleResponse):
        pass

    @rule_test('email_notification_off', should_alert=True)
    def test_email_notification_off(self, rule_result: RuleResponse):
        pass
