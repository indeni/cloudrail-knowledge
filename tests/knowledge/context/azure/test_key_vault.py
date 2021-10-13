from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestKeyVault(AzureContextTest):

    def get_component(self):
        return "key_vault"

    @context(module_path="name_only")
    def test_name_only(self, ctx: AzureEnvironmentContext):
        key_vault = next((key_vault for key_vault in ctx.key_vaults if key_vault.name == 'cr2388-keyvault'), None)
        self.assertIsNotNone(key_vault)
        self.assertFalse(key_vault.purge_protection_enabled)

    @context(module_path="purge_protection_disabled_default")
    def test_purge_protection_disabled_default(self, ctx: AzureEnvironmentContext):
        key_vault = next((key_vault for key_vault in ctx.key_vaults if key_vault.name == 'cr24041-keyvault'), None)
        self.assertIsNotNone(key_vault)
        self.assertFalse(key_vault.purge_protection_enabled)

    @context(module_path="purge_protection_enabled")
    def test_purge_protection_enabled(self, ctx: AzureEnvironmentContext):
        key_vault = next((key_vault for key_vault in ctx.key_vaults if key_vault.name == 'cr24041-keyvault'), None)
        self.assertIsNotNone(key_vault)
        self.assertTrue(key_vault.purge_protection_enabled)
