from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_transparent_data_encryption import AzureMsSqlServerTransparentDataEncryption
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SqlServerTransparentEncryptionDataBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureMsSqlServerTransparentDataEncryption:
        return AzureMsSqlServerTransparentDataEncryption(server_id=attributes['server_id'],
                                                         key_vault_key_id=self._get_known_value(attributes, 'key_vault_key_id'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MSSQL_SERVER_TRANSPARENT_DATA_ENCRYPTION
