from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestSecurityCenterAutoProvisioning(AzureContextTest):

    def get_component(self):
        return 'security_center_auto_provisioning'

    @context(module_path='auto_provisioning_on')
    def test_auto_provisioning_on(self, ctx: AzureEnvironmentContext):
        scap = ctx.security_center_auto_provisioning.values().pop()
        self.assertTrue(scap.auto_provision_is_on)

    @context(module_path='auto_provisioning_off')
    def test_auto_provisioning_off(self, ctx: AzureEnvironmentContext):
        scap = ctx.security_center_auto_provisioning.values().pop()
        self.assertFalse(scap.auto_provision_is_on)
