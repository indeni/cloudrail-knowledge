from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.batch_management.azure_batch_account import BatchAccountPoolAllocationMode
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestBatchAccount(AzureContextTest):

    def get_component(self):
        return "batch_account"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        batch_account = next((batch for batch in ctx.batch_accounts if batch.server_name == 'cloudrailtestbatchacc'), None)
        self.assertIsNotNone(batch_account)
        self.assertEqual(batch_account.pool_allocation_mode, BatchAccountPoolAllocationMode.USER_SUBSCRIPTION)
        self.assertFalse(batch_account.public_network_access_enabled)
        self.assertTrue(batch_account.key_vault_reference)
        self.assertEqual(batch_account.key_vault_reference.server_name, 'cloudrailtestbatchacc')
        if batch_account.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(batch_account.key_vault_reference.id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cloudrailtest-rg/providers/Microsoft.KeyVault/vaults/cloudrailtestkeyvault')
            self.assertEqual(batch_account.key_vault_reference.url,
                             'https://cloudrailtestkeyvault.vault.azure.net/')
            self.assertEqual(batch_account.storage_account_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cloudrailtest-rg/providers/Microsoft.Storage/storageAccounts/cloudrailteststorageacc')
        elif batch_account.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(batch_account.key_vault_reference.id,
                             'azurerm_key_vault.test.id')
            self.assertEqual(batch_account.key_vault_reference.url,
                             'azurerm_key_vault.test.vault_uri')
            self.assertEqual(batch_account.storage_account_id,
                             'azurerm_storage_account.test.id')
