from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestStorageAccountCustomerManagedKey(AzureContextTest):

    def get_component(self):
        return "storage_account_customer_managed_key"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):

        customer_managed_key = next((customer_managed_key for customer_managed_key in ctx.storage_accounts_customer_managed_key
                                    if customer_managed_key.get_id() in
                                    ['/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2498-RG/providers/Microsoft.Storage/storageAccounts/cr2498tststacc',
                                     'azurerm_storage_account_customer_managed_key.example.id']), None)
        self.assertIsNotNone(customer_managed_key)
        self.assertEqual(customer_managed_key.key_name, 'cr2498-key')

        if customer_managed_key.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(customer_managed_key.key_vault_uri, 'https://cr2498-keyvault.vault.azure.net/')
            self.assertEqual(customer_managed_key.storage_account_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2498-RG/providers/Microsoft.Storage/storageAccounts/cr2498tststacc')
            self.assertEqual(customer_managed_key.key_vault_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2498-RG/providers/Microsoft.KeyVault/vaults/cr2498-keyvault')
        elif customer_managed_key.origin == EntityOrigin.TERRAFORM:
            self.assertIsNone(customer_managed_key.key_vault_uri)
            self.assertEqual(customer_managed_key.storage_account_id, 'azurerm_storage_account.storacc.id')
            self.assertEqual(customer_managed_key.key_vault_id, 'azurerm_key_vault.kv.id')



