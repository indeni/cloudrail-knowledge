from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_analytics_account import DataLakeAnalyticsAccountTier

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestDataLakeAnalyticsAccount(AzureContextTest):

    def get_component(self):
        return "data_lake_analytics_account"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        data_lake_analytics_account = next((data for data in ctx.data_lake_analytics_accounts
                                            if data.server_name == 'cr3682datalakeacc'), None)
        self.assertIsNotNone(data_lake_analytics_account)
        self.assertEqual(data_lake_analytics_account.default_store_account_name, 'cr3682datalakest')
        self.assertEqual(data_lake_analytics_account.tier, DataLakeAnalyticsAccountTier.CONSUMPTION)
        self.assertEqual(len(data_lake_analytics_account.monitor_diagnostic_settings), 1)
        self.assertEqual(data_lake_analytics_account.monitor_diagnostic_settings[0].server_name, 'cr3682diag')
