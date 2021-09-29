from cloudrail.knowledge.context.azure.resources.keyvault.azure_key_vault import AzureKeyVault

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class KeyVaultBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'key-vaults-list.json'

    def do_build(self, attributes: dict) -> AzureKeyVault:
        return AzureKeyVault(attributes['name'], attributes['properties'].get('enablePurgeProtection', False))
