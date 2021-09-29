from cloudrail.knowledge.context.azure.resources.databases.azure_mysql_server import AzureMySqlServer
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class MySqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'mysql-servers-list.json'

    def do_build(self, attributes: dict) -> AzureMySqlServer:
        return AzureMySqlServer(server_name=attributes['name'],
                                ssl_enforcement_enabled=attributes['properties']['sslEnforcement'] == 'Enabled')
