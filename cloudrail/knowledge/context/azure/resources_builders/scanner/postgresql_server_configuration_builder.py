
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AzurePostgreSqlServerConfigurationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'postgresql-configuration-list.json'

    def do_build(self, attributes: dict) -> AzurePostgreSqlServerConfiguration:
        properties = attributes['properties']
        server_name = attributes['id'].split('servers/')[1].split('/')[0]
        return AzurePostgreSqlServerConfiguration(server_name=server_name,
                                                  name=attributes['name'],
                                                  value=properties['value'])
