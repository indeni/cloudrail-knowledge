from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import ManagedIdentityType
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_store import AzureDataLakeStore, DataLakeStoreTier
from cloudrail.knowledge.context.field_active import FieldActive
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestDataLakeStore(AzureContextTest):

    def get_component(self):
        return "data_lake_store"

    @context(module_path="default_settings")
    def test_default_settings(self, ctx: AzureEnvironmentContext):
        data_store: AzureDataLakeStore = ctx.data_lake_store.get('cr3682datalakesto')
        self.assertIsNotNone(data_store)
        self.assertEqual(data_store.tier, DataLakeStoreTier.CONSUMPTION)
        self.assertEqual(data_store.encryption_state, FieldActive.ENABLED)
        self.assertEqual(data_store.encryption_type, 'ServiceManaged')
        self.assertEqual(len(data_store.managed_identities), 1)
        self.assertEqual(data_store.managed_identities[0].identity_type, ManagedIdentityType.SYSTEM_ASSIGNED)
        self.assertEqual(data_store.firewall_allow_azure_ips, FieldActive.ENABLED)
        self.assertEqual(data_store.firewall_state, FieldActive.ENABLED)
        self.assertEqual(len(data_store.monitor_diagnostic_settings), 1)

    @context(module_path="custom_settings")
    def test_custom_settings(self, ctx: AzureEnvironmentContext):
        data_store: AzureDataLakeStore = ctx.data_lake_store.get('cr3682datalakesto')
        self.assertIsNotNone(data_store)
        self.assertEqual(data_store.tier, DataLakeStoreTier.COMMITMENT_1TB)
        self.assertEqual(data_store.encryption_state, FieldActive.DISABLED)
        self.assertEqual(data_store.encryption_type, '')
        self.assertEqual(len(data_store.managed_identities), 1)
        self.assertEqual(data_store.managed_identities[0].identity_type, ManagedIdentityType.SYSTEM_ASSIGNED)
        self.assertEqual(data_store.firewall_allow_azure_ips, FieldActive.DISABLED)
        self.assertEqual(data_store.firewall_state, FieldActive.DISABLED)
        self.assertEqual(data_store.tags, {})
        self.assertEqual(len(data_store.monitor_diagnostic_settings), 1)
