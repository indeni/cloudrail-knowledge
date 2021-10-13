from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestAzureCosmosDBAccount(AzureContextTest):

    def get_component(self):
        return "cosmos_db_account"

    # Not running drift detection since i am unable to create drift data (permission issue)
    @context(module_path="cosmos_db_account", test_options=TestOptions(run_drift_detection=False))
    def test_cosmos_db_account(self, ctx: AzureEnvironmentContext):
        cosmos_db_account = next((disk for disk in ctx.cosmos_db_account if disk.resource_group_name == 'crtest-rg'), None)
        self.assertIsNotNone(cosmos_db_account)
        self.assertEqual(cosmos_db_account.kind, 'MongoDB')

    @context(module_path="cosmos_db_account_2", test_options=TestOptions(run_drift_detection=False))
    def test_cosmos_db_account2(self, ctx: AzureEnvironmentContext):
        cosmos_db_account = next((disk for disk in ctx.cosmos_db_account if disk.resource_group_name == 'cloudrailtest2-rg'),
                                 None)
        self.assertIsNotNone(cosmos_db_account)
        self.assertEqual(cosmos_db_account.kind, 'GlobalDocumentDB')
