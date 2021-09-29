from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SqlServerExtendedAuditingPolicyBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSqlServerExtendedAuditingPolicy:
        return AzureSqlServerExtendedAuditingPolicy(server_id=attributes['server_id'],
                                                    retention_in_days=self._get_known_value(attributes, 'retention_in_days', 0),
                                                    log_monitoring_enabled=self._get_known_value(attributes, 'log_monitoring_enabled', False))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MSSQL_SERVER_EXTENDED_AUDITING_POLICY
