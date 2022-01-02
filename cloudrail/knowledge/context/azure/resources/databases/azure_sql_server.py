from typing import Optional, List
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_transparent_data_encryption import AzureMsSqlServerTransparentDataEncryption
from cloudrail.knowledge.context.azure.resources.i_managed_identity_resource import IManagedIdentityResource
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity


class MsSqlServerVersion(str, Enum):
    VERSION_2_0 = '2.0'
    VERSION_12_0 = '12.0'


class MsSqlServerConnectionPolicy(str, Enum):
    DEFAULT = 'Default'
    PROXY = 'Proxy'
    REDIRECT = 'Redirect'

class MsSqlServerMinimumTLSVersion(str, Enum):
    VERSION_1_0 = '1.0'
    VERSION_1_1 = '1.1'
    VERSION_1_2 = '1.2'


@dataclass
class MsSqlServerAzureAdAdministrator:
    """
        Attributes:
            login_username: The login username of the Azure AD Administrator of this SQL Server.
            object_id: The object id of the Azure AD Administrator of this SQL Server.
            tenant_id: The tenant id of the Azure AD Administrator of this SQL Server.
            azuread_authentication_only: Specifies whether only AD Users and administrators can be used to login or also local database users.
    """
    login_username: str
    object_id: str
    tenant_id: str
    azuread_authentication_only: bool

class AzureSqlServer(AzureResource, IManagedIdentityResource):
    """
        Attributes:
            server_name: The name of the SQL server
            azuread_administrator_list: A list (only 1 element supported) of AD Administrator for this server.
            identity_list: A list of identities (only 1 element supported) to be used by this server.
            minimum_tls_version: The Minimum TLS Version for all SQL Database and SQL Data Warehouse databases associated with the server.
            public_network_access_enabled: Whether public network access is allowed for this server.
            primary_user_assigned_identity_id: Specifies the primary user managed identity id.
            public_network_access_enabled: An indication on if public network access is enabled.
            managed_identities: All managed identities associate with the SQL server.
            user_assigned_identity_ids: List of User Assigned Identity IDs, if any associated with the SQL server.
    """

    def __init__(self,
                 server_name: str,
                 version: MsSqlServerVersion,
                 administrator_login: str,
                 azuread_administrator_list: Optional[List[MsSqlServerAzureAdAdministrator]],
                 user_assigned_identity_ids: Optional[List[str]],
                 managed_identities: List[AzureManagedIdentity],
                 minimum_tls_version: Optional[MsSqlServerMinimumTLSVersion],
                 primary_user_assigned_identity_id: Optional[str],
                 public_network_access_enabled: bool) -> None:
        super().__init__(AzureResourceType.AZURERM_SQL_SERVER)
        self.server_name: str = server_name
        self.with_aliases(server_name)
        self.version: MsSqlServerVersion = version
        self.administrator_login: str = administrator_login
        self.azuread_administrator_list: Optional[List[MsSqlServerAzureAdAdministrator]
                                                  ] = azuread_administrator_list
        self.minimum_tls_version: Optional[MsSqlServerMinimumTLSVersion] = minimum_tls_version
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.user_assigned_identity_ids: List[str] = user_assigned_identity_ids
        self.managed_identities: List[AzureManagedIdentity] = managed_identities
        self.primary_user_assigned_identity_id: Optional[str] = primary_user_assigned_identity_id
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.security_alert_policy_list: Optional[List[AzureMsSqlServerSecurityAlertPolicy]] = []
        self.transparent_data_encryption: Optional[AzureMsSqlServerTransparentDataEncryption] = None
        self.extended_auditing_policy: AzureSqlServerExtendedAuditingPolicy = None

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

    def get_type(self, is_plural: bool = False) -> str:
        return 'Asure SQL server ' + ('s' if is_plural else '')

    def get_managed_identities(self) -> List[AzureManagedIdentity]:
        return self.managed_identities

    def get_managed_identities_ids(self) -> List[str]:
        return self.user_assigned_identity_ids

    def to_drift_detection_object(self) -> dict:
        return {'server_name': self.server_name,
                'public_network_access_enabled': self.public_network_access_enabled,
                'managed_identities': [identity.to_drift_detection_object() for identity in self.managed_identities],}
