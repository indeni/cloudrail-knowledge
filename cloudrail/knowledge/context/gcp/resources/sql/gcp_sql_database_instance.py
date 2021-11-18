from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource

import dataclasses


class GcpSqlDBInstanceType(Enum):
    SQL_INSTANCE_TYPE_UNSPECIFIED = 'SQL_INSTANCE_TYPE_UNSPECIFIED'
    CLOUD_SQL_INSTANCE = 'CLOUD_SQL_INSTANCE'
    ON_PREMISES_INSTANCE = 'ON_PREMISES_INSTANCE'
    READ_REPLICA_INSTANCE = 'READ_REPLICA_INSTANCE'


class GcpSqlDBInstanceVersion(Enum):
    MYSQL56 = 'MYSQL_5_6'
    MYSQL57 = 'MYSQL_5_7'
    MYSQL80 = 'MYSQL_8_0'
    POSTGRES96 = 'POSTGRES_9_6'
    POSTGRES10 = 'POSTGRES_10'
    POSTGRES11 = 'POSTGRES_11'
    POSTGRES12 = 'POSTGRES_12'
    POSTGRES13 = 'POSTGRES_13'
    SQLSERVER_2017_STANDARD = 'SQLSERVER_2017_STANDARD'
    SQLSERVER_2017_ENTERPRISE = 'SQLSERVER_2017_ENTERPRISE'
    SQLSERVER_2017_EXPRESS = 'SQLSERVER_2017_EXPRESS'
    SQLSERVER_2017_WEB = 'SQLSERVER_2017_WEB'
    SQLSERVER_2019_STANDARD = 'SQLSERVER_2019_STANDARD'
    SQLSERVER_2019_ENTERPRISE = 'SQLSERVER_2019_ENTERPRISE'
    SQLSERVER_2019_EXPRESS = 'SQLSERVER_2019_EXPRESS'
    SQLSERVER_2019_WEB = 'SQLSERVER_2019_WEB'


@dataclass
class GcpSqlDBInstanceSettingsDBFlags:
    """
        Attributes:
            name: (Required) Name of the flag.
            value: (Required) Value of the flag.
    """
    name: str
    value: str


@dataclass
class GcpSqlDBInstanceSettingsBackupRetention:
    """
        Attributes:
            retained_backups: (Required) Depending on the value of retention_unit, this is used to determine if a backup needs to be deleted.
            retention_unit: (Optional) The unit that 'retained_backups' represents. Defaults to COUNT.
    """
    retained_backups: int
    retention_unit: Optional[str]


@dataclass
class GcpSqlDBInstanceSettingsBackupConfig:
    """
        Attributes:
            binary_log_enabled: (Optional) True if binary logging is enabled. Applicable for MySql only.
            enabled: (Optional) True if backup configuration is enabled.
            start_time: (Optional) HH:MM format time indicating when backup configuration starts.
            point_in_time_recovery_enabled: (Optional) True if Point-in-time recovery is enabled. Applicable for PostGres only.
            location: (Optional) The region where the backup will be stored.
            transaction_log_retention_days: (Optional) The number of days of transaction logs retained for point in time restore, from 1-7.
            backup_retention_settings: (Optional) A subblock of backup retention configuration parameters.
    """
    binary_log_enabled: Optional[bool]
    enabled: Optional[bool]
    start_time: Optional[datetime]
    point_in_time_recovery_enabled: Optional[bool]
    location: Optional[str]
    transaction_log_retention_days: Optional[int]
    backup_retention_settings: Optional[GcpSqlDBInstanceSettingsBackupRetention]


@dataclass
class GcpSqlDBInstanceIPConfigAuthNetworks:
    """
        Attributes:
            expiration_time: (Optional) The RFC 3339 formatted date time string indicating when this whitelist expires.
            name: (Optional) A name for this whitelist entry.
            value: (Required) A CIDR notation IPv4 or IPv6 address that is allowed to access this instance. Must be set even if other two attributes are not for the whitelist to become active.
    """
    expiration_time: Optional[datetime]
    name: Optional[str]
    value: str


@dataclass
class GcpSqlDBInstanceSettingsIPConfig:
    """
        Attributes:
            ipv4_enabled: (Optional) If the Sql instance should be assigned a public ipv4 address. Either ipv4_enabled must be enabled or a private_network must be configured.
            private_network: (Optional) The VPC network from which the Cloud SQL instance is accessible for private IP.
            require_ssl: (Optional) An indication if this instance requires SSL or not.
            authorized_networks: (Optional) A sublist that specifies networks authorized to access the resources.
    """
    ipv4_enabled: Optional[bool]
    private_network: Optional[str]
    require_ssl: Optional[bool]
    authorized_networks: Optional[List[GcpSqlDBInstanceIPConfigAuthNetworks]]


@dataclass
class GcpSqlDBInstanceSettings:
    """
        Attributes:
            tier: (Required) The machine type to use.
            database_flags: (Optional) A sublist to support database flags. A "name" and "value" are required.
            backup_configuration: (Optional) A subblock of backup configuration parameters.
            ip_configuration: (Optional) A sublock of IP configuration parameters.
    """
    tier: str
    database_flags: Optional[List[GcpSqlDBInstanceSettingsDBFlags]]
    backup_configuration: Optional[GcpSqlDBInstanceSettingsBackupConfig]
    ip_configuration: Optional[GcpSqlDBInstanceSettingsIPConfig]


class GcpSqlDatabaseInstance(GcpResource):
    """
        Attributes:
            name: (Optional, Computed) The name of this SQL database instance.
            region: (Optional) The region where this instance resides.
            settings: (Optional) The settings used for the sql instance.
            database_version: (Optional, Default: MYSQL_5_6) The version of the sql database.
    """

    def __init__(self,
                 name: str,
                 region: str,
                 settings: Optional[GcpSqlDBInstanceSettings],
                 database_version: Optional[GcpSqlDBInstanceVersion]):

        super().__init__(GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE)
        self.name: Optional[str] = name
        self.region: Optional[str] = region
        self.settings: Optional[GcpSqlDBInstanceSettings] = settings
        self.database_version: Optional[GcpSqlDBInstanceVersion] = database_version


    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_labeled(self) -> bool:
        return True

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/sql/instances/{self.name}/'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SQL Database Instance'
        else:
            return 'SQL Database Instances'

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'settings': self.settings and dataclasses.asdict(self.settings),
                'labels': self.labels}
