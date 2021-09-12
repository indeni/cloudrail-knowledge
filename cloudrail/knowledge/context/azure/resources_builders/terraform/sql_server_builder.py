from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SqlServerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSqlServer:
        sql_server = AzureSqlServer(server_name=attributes['name'],
                                    public_network_access_enable=attributes['public_network_access_enabled'])
        if audit_policy := self._get_known_value(attributes, 'extended_auditing_policy'):
            sql_server.extended_auditing_policy = AzureSqlServerExtendedAuditingPolicy(server_id=attributes['id'],
                                                                                       retention_in_days=self._get_known_value(audit_policy[0], 'retention_in_days', 0),
                                                                                       log_monitoring_enabled=self._get_known_value(audit_policy[0], 'log_monitoring_enabled', False))
        return sql_server

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MSSQL_SERVER
