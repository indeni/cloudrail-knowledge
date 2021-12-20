from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureNoCloudAccountContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestNoCloudAccount(AzureNoCloudAccountContextTest):

    def get_component(self):
        return 'no_cloud_account'

    @context(module_path="nsg", test_options=TestOptions(run_cloudmapper=False))
    def test_role_no_cloud_account(self, ctx: AzureEnvironmentContext):
        nsg = next((nsg for nsg in ctx.net_security_groups if nsg.name == 'no-cloud-account-nsg'), None)
        self.assertIsNotNone(nsg)
        self.assertEqual(nsg.subscription_id, '00000000-0000-0000-0000-000000000000')
        self.assertEqual(nsg.tenant_id, '00000000-0000-0000-0000-000000000000')
