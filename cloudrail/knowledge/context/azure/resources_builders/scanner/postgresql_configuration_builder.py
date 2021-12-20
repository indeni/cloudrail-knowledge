
from cloudrail.knowledge.context.azure.resources.databases.postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AzurePostgreSqlServerConfigurationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'postgresql-servers-list.json'

    def do_build(self, attributes: dict) -> AzurePostgreSqlServerConfiguration:
        properties = attributes['properties']
        server_name = properties['id'].splir('servers/')[1].split('/')[0]
        return AzurePostgreSqlServerConfiguration(server_name=server_name,
                                                  name=properties['name'],
                                                  value=properties['value'])
