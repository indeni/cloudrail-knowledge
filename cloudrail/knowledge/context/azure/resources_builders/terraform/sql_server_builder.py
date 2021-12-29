from typing import Callable, List
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer, MsSqlServerVersion, MsSqlServerAzureAdAdministrator, \
    MsSqlServerMinimumTLSVersion
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_terraform_user_managed_identities_ids, \
    create_terraform_system_managed_identity


class MsSqlServerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSqlServer:
        sql_server = _sql_server_builder(attributes, self._get_known_value)
        if audit_policy := self._get_known_value(attributes, 'extended_auditing_policy'):
            sql_server.extended_auditing_policy = AzureSqlServerExtendedAuditingPolicy(server_id=attributes['id'],
                                                                                       retention_in_days=self._get_known_value(audit_policy[0], 'retention_in_days', 0),
                                                                                       log_monitoring_enabled=self._get_known_value(audit_policy[0], 'log_monitoring_enabled', False))
        return sql_server

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MSSQL_SERVER

class StandardSqlServerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSqlServer:

        return _sql_server_builder(attributes, self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SQL_SERVER

def _sql_server_builder(attributes: dict, get_known_value: Callable) -> AzureSqlServer:
    ## Azure admin list
    azuread_administrator_list: List[MsSqlServerAzureAdAdministrator] = []
    for azure_admin in get_known_value(attributes, 'azuread_administrator', []):
        azuread_administrator_list.append(MsSqlServerAzureAdAdministrator(login_username=azure_admin['login_username'],
                                                                          object_id=azure_admin['object_id'],
                                                                          tenant_id=get_known_value(azure_admin, 'tenant_id'),
                                                                          azuread_authentication_only=get_known_value(azure_admin,
                                                                                                                      'azuread_authentication_only')))
    ## Managed Identities
    managed_identities: List[AzureManagedIdentity] = []
    if managed_identity := create_terraform_system_managed_identity(attributes):
        managed_identities.append(managed_identity)

    return AzureSqlServer(server_name=attributes['name'],
                          version=enum_implementation(MsSqlServerVersion, attributes['version']),
                          administrator_login=attributes['administrator_login'],
                          azuread_administrator_list=azuread_administrator_list,
                          user_assigned_identity_ids=get_terraform_user_managed_identities_ids(attributes),
                          managed_identities=managed_identities,
                          minimum_tls_version=enum_implementation(MsSqlServerMinimumTLSVersion, get_known_value(attributes, 'minimum_tls_version')),
                          primary_user_assigned_identity_id=get_known_value(attributes, 'primary_user_assigned_identity_id'),
                          public_network_access_enabled=get_known_value(attributes, 'public_network_access_enabled'))
