from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class PostgreSqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'postgresql-servers-list.json'

    def do_build(self, attributes: dict) -> AzurePostgreSqlServer:
        return AzurePostgreSqlServer(server_name=attributes['name'],
                                     ssl_enforcement_enabled=attributes['properties']['sslEnforcement'] == 'Enabled')
