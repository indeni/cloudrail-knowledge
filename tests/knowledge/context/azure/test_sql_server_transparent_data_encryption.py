from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlServerTransparentDataEncryption(AzureContextTest):

    def get_component(self):
        return "sql_server_transparent_data_encryption"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        encrypt_data = next((data for data in ctx.sql_server_transparent_data_encryptions
                             if data.server_id in ('azurerm_mssql_server.sql.id', 'cr2523-sqlserver')), None)
        self.assertIsNotNone(encrypt_data)
        self.assertTrue(encrypt_data.key_vault_key_id in ('https://cr2523-keyvault.vault.azure.net/keys/cr2523-sqlkey/102c284260c94b2290745bb3487fa40b',
                                                          'azurerm_key_vault_key.key.id'))
