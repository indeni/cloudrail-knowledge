from cloudrail.knowledge.context.azure.resources.databases.azure_database_configuration import AzureDatabaseConfiguration
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class PostgreSqlServerConfigurationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'postgresql-server-configurations.json'

    def do_build(self, attributes: dict) -> AzureDatabaseConfiguration:
        server_name = attributes['id'].split("/", 9)[8]
        return AzureDatabaseConfiguration(name=attributes['name'],
                                          server_name=server_name,
                                          value=attributes['properties']['value'])
