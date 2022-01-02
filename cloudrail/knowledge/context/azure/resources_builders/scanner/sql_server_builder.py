from typing import List
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer, MsSqlServerVersion, MsSqlServerAzureAdAdministrator, \
    MsSqlServerMinimumTLSVersion
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_scanner_system_managed_identity, \
    get_scanner_user_managed_identities_ids
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class SqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-list.json'

    def do_build(self, attributes: dict) -> AzureSqlServer:
        properties = attributes['properties']
        ## Azure admin list
        azuread_administrator_list: List[MsSqlServerAzureAdAdministrator] = []
        if azure_admin := properties.get('administrators'):
            azuread_administrator_list.append(MsSqlServerAzureAdAdministrator(login_username=azure_admin['login'],
                                                                              object_id=azure_admin['sid'],
                                                                              tenant_id=azure_admin['tenantId'],
                                                                              azuread_authentication_only=azure_admin['azureADOnlyAuthentication']))
        ## Managed Identities
        managed_identities: List[AzureManagedIdentity] = []
        if managed_identity := create_scanner_system_managed_identity(attributes):
            managed_identities.append(managed_identity)

        return AzureSqlServer(server_name=attributes['name'],
                              version=enum_implementation(MsSqlServerVersion, properties['version']),
                              administrator_login=properties['administratorLogin'],
                              azuread_administrator_list=azuread_administrator_list,
                              user_assigned_identity_ids=get_scanner_user_managed_identities_ids(attributes),
                              managed_identities=managed_identities,
                              minimum_tls_version=enum_implementation(MsSqlServerMinimumTLSVersion, properties.get('minimalTlsVersion')),
                              primary_user_assigned_identity_id=properties.get('primaryUserAssignedIdentityId'),
                              public_network_access_enabled=properties['publicNetworkAccess'] == 'Enabled')
