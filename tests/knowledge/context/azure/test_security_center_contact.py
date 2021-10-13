from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSecurityCenterContact(AzureContextTest):

    def get_component(self):
        return "security_center_contact"

    @context(module_path="email_notification_off")
    def test_email_notifications_off(self, ctx: AzureEnvironmentContext):
        scc = ctx.security_center_contacts.values().pop()
        self.assertFalse(scc.alert_notifications)

    @context(module_path="email_notification_on")
    def test_email_notifications_on(self, ctx: AzureEnvironmentContext):
        scc = ctx.security_center_contacts.values().pop()
        self.assertTrue(scc.alert_notifications)
