from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder

class SqlServerExtendedAuditingPolicyBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-server-auditing.json'

    def do_build(self, attributes: dict) -> AzureSqlServerExtendedAuditingPolicy:
        return AzureSqlServerExtendedAuditingPolicy(server_id=attributes['id'].replace('/extendedAuditingSettings/Default', ''),
                                                    log_monitoring_enabled=attributes['properties']['state'] == 'Enabled',
                                                    retention_in_days=attributes['properties']['retentionDays'])
