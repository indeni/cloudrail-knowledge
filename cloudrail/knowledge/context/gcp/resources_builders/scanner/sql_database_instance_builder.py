from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance

from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class SqlDatabaseInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'sqladmin-v1beta4-instances-list.json'

    def do_build(self, attributes: dict) -> GcpSqlDatabaseInstance:
        settings = attributes['settings']
        ip_configuration = settings['ipConfiguration']
        require_ssl = ip_configuration.get('requireSsl', False)

        return GcpSqlDatabaseInstance(name=attributes['name'],
                                      require_ssl=require_ssl)
