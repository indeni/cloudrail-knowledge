from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_transparent_data_encryption import AzureMsSqlServerTransparentDataEncryption
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder

class SqlServerTransparentEncryptionDataBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-encryption-protectors.json'

    def do_build(self, attributes: dict) -> AzureMsSqlServerTransparentDataEncryption:
        properties = attributes['properties']
        if properties['serverKeyType'] == 'AzureKeyVault':
            return AzureMsSqlServerTransparentDataEncryption(server_id=attributes['id'].split('/')[-3],
                                                            key_vault_key_id=properties['uri'])
        return None
