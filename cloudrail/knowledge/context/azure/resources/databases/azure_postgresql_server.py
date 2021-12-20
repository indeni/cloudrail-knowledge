from typing import Optional, Dict, List
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.databases.postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration


class PostgreSqlServerVersion(Enum):
    VERSION_9_5 = '9.5'
    VERSION_9_6 = '9.6'
    VERSION_10 = '10'
    VERSION_10_0 = '10.0'
    VERSION_11 = '11'


class PostgreSqlServerIdentityType(Enum):
    SYSTEM_ASSIGNED = 'SystemAssigned'


class PostgreSqlServerThreatDetectionPolicyAlerts(Enum):
    ACCESS_ANOMALY = 'Access_Anomaly'
    SQL_INJECTION = 'Sql_Injection'
    SQL_INJECTION_VULNERABILITY = 'Sql_Injection_Vulnerability'


@dataclass
class PostgreSqlServerIdentity:
    """
    Attributes:
        type: The type of identity used for the PostgreSQL server.
    """
    type: PostgreSqlServerIdentityType


@dataclass
class PostgreSqlServerThreatDetectionPolicy:
    """
        Attributes:
            enabled: If the Threat Detection Policy is enabled or not.
            disabled_alerts: List of alerts which should be disabled.
            email_account_admins: If account administrators should be emailed when an alert is triggered.
            email_addresses: A list of email addresses which alerts should be sent to.
            retention_days: Specifies the number of days to keep in the Threat Detection audit logs.
            storage_account_access_key: Specifies the identifier key of the Threat Detection audit storage account.
            storage_endpoint: Specifies the blob storage endpoint. This blob storage will hold all Threat Detection audit logs.
    """
    enabled: bool
    disabled_alerts: Optional[List[PostgreSqlServerThreatDetectionPolicyAlerts]]
    email_account_admins: Optional[bool]
    email_addresses: Optional[List[str]]
    retention_days: Optional[int]
    storage_account_access_key: str
    storage_endpoint: str


class AzurePostgreSqlServer(AzureResource):
    """
        Attributes:
            server_name: The name of the PostgreSQL Server.
            sku_name: The SKU name for this PostgreSQL Server.
            version: The version of PostgreSQL to use.
            administrator_login: The Administrator Login for the PostgreSQL Server.
            auto_grow_enabled: Enable/Disable auto-growing of the storage.
            backup_retention_days: Backup retention days for the server.
            geo_redundant_backup_enabled: Turn Geo-redundant server backups on/off.
            identity: The identity used for the PostgreSQL server.
            infrastructure_encryption_enabled: Whether or not infrastructure is encrypted for this server.
            public_network_access_enabled: Whether or not public network access is allowed for this server.
            ssl_enforcement_enabled: Specifies if SSL should be enforced on connections.
            ssl_minimal_tls_version_enforced: The mimimun TLS version to support on the sever.
            storage_mb: Max storage allowed for a server.
    """

    def __init__(self,
                 server_name: str,
                 sku_name: str,
                 version: PostgreSqlServerVersion,
                 administrator_login: Optional[str],
                 auto_grow_enabled: bool,
                 backup_retention_days: Optional[int],
                 geo_redundant_backup_enabled: Optional[bool],
                 identity: Optional[PostgreSqlServerIdentity],
                 infrastructure_encryption_enabled: bool,
                 public_network_access_enabled: bool,
                 ssl_enforcement_enabled: bool,
                 ssl_minimal_tls_version_enforced: str,
                 storage_mb: Optional[int],
                 tags: Dict[str, str] = None):
        super().__init__(AzureResourceType.AZURERM_POSTGRESQL_SERVER)
        self.name: str = server_name
        self.with_aliases(server_name)
        if tags:
            self.tags = tags
        self.sku_name: str = sku_name
        self.version: PostgreSqlServerVersion = version
        self.administrator_login: Optional[str] = administrator_login
        self.auto_grow_enabled: bool = auto_grow_enabled
        self.backup_retention_days: Optional[int] = backup_retention_days
        self.geo_redundant_backup_enabled: Optional[bool] = geo_redundant_backup_enabled
        self.identity: Optional[PostgreSqlServerIdentity] = identity
        self.infrastructure_encryption_enabled: bool = infrastructure_encryption_enabled
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.ssl_enforcement_enabled: bool = ssl_enforcement_enabled
        self.ssl_minimal_tls_version_enforced: str = ssl_minimal_tls_version_enforced
        self.storage_mb: Optional[int] = storage_mb
        self.postgresql_configuration: Optional[AzurePostgreSqlServerConfiguration] = None

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}' \
               f'/resourceGroups/{self.resource_group_name}/providers/Microsoft.DBForPostgreSQL/servers/{self.name}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'PostgreSQL Server'
        else:
            return 'PostgreSQL Servers'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags,
                'name': self.name,
                'ssl_enforcement_enabled': self.ssl_enforcement_enabled}
