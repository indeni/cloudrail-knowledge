from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.keyvault.azure_key_vault import AzureKeyVault

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class KeyVaultBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureKeyVault:
        return AzureKeyVault(name=attributes['name'], purge_protection_enabled=self._get_known_value(attributes, 'purge_protection_enabled', False))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_KEY_VAULT
