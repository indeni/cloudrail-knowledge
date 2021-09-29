from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-list.json'

    def do_build(self, attributes: dict) -> AzureSqlServer:
        return AzureSqlServer(server_name=attributes['name'],
                              public_network_access_enable=attributes['properties']['publicNetworkAccess'] == 'Enabled')
