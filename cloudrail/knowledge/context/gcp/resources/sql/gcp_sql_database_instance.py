from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


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
class GcpSqlDBInstanceSettingsLocPref:
    """
        Attributes:
            follow_gae_application: (Optional) A GAE application whose zone to remain in. Must be in the same region as this instance.
            zone: (Optional) The preferred compute engine zone.
    """
    follow_gae_application: Optional[str]
    zone: Optional[str]


@dataclass
class GcpSqlDBInstanceSettingsMaintWindow:
    """
        Attributes:
            day: (Optional) Day of week (1-7), starting on Monday.
            hour: (Optional) Hour of day (0-23), ignored if day not set.
            update_track: (Optional) Receive updates earlier (canary) or later (stable).
    """
    day: Optional[int]
    hour: Optional[int]
    update_track: Optional[str]


@dataclass
class GcpSqlDBInstanceSettingsInsights:
    """
        Attributes:
            query_insights_enabled: (Optional) True if Query Insights feature is enabled.
            query_string_length: (Optional) Maximum query length stored in bytes. Between 256 and 4500. Default to 1024.
            record_application_tags: (Optional) True if Query Insights will record application tags from query when enabled.
            record_client_address: (Optional) True if Query Insights will record client address when enabled.
    """
    query_insights_enabled: Optional[bool]
    query_string_length: Optional[int]
    record_application_tags: Optional[bool]
    record_client_address: Optional[bool]


@dataclass
class GcpSqlDBInstanceSettings:
    """
        Attributes:
            tier: (Required) The machine type to use.
            activation_policy: (Optional) This specifies when the instance should be active.
            authorized_gae_applications: (Optional, Deprecated) This property is only applicable to First Generation instances.
            availability_type: (Optional) The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL).
            collation: (Optional) The name of server instance collation.
            crash_safe_replication: (Optional, Deprecated) (Applicable to First Generation instances) Specific to read instances, indicates when crash-safe replication flags are enabled.
            disk_autoresize: (Optional, Default: true) Configuration to increase storage size automatically.
            disk_size: (Optional, Default: 10) The size of data disk, in GB.
            disk_type: (Optional, Default: PD_SSD) The type of data disk. Available options are PD_SSD and PD_HDD.
            pricing_plan: (Optional) Pricing plan for this instance, can only be PER_USE.
            replication_type: (Optional, Deprecated) This property is only applicable to First Generation instances. Replication type for this instance, can be one of ASYNCHRONOUS or SYNCHRONOUS.
            user_labels: (Optional) A set of key/value user label pairs to assign to the instance.
            database_flags: (Optional) A sublist to support database flags. A "name" and "value" are required.
            backup_configuration: (Optional) A subblock of backup configuration parameters.
            ip_configuration: (Optional) A sublock of IP configuration parameters.
            location_preference: (Optional) A subblock of location preference parameters.
            maintenance_window: (Optional) A subblock of maintenance window parameters.
            insights_config: (Optional) A subblock for instances to declare Query Insights configuration.
    """
    tier: str
    activation_policy: Optional[int]
    authorized_gae_applications: Optional[List[str]]
    availability_type: Optional[str]
    collation: Optional[str]
    crash_safe_replication: Optional[bool]
    disk_autoresize: Optional[bool]
    disk_size: Optional[int]
    disk_type: Optional[str]
    pricing_plan: Optional[str]
    replication_type: Optional[str]
    user_labels: Optional[dict]
    database_flags: Optional[List[GcpSqlDBInstanceSettingsDBFlags]]
    backup_configuration: Optional[GcpSqlDBInstanceSettingsBackupConfig]
    ip_configuration: Optional[GcpSqlDBInstanceSettingsIPConfig]
    location_preference: Optional[GcpSqlDBInstanceSettingsLocPref]
    maintenance_window: Optional[GcpSqlDBInstanceSettingsMaintWindow]
    insights_config: Optional[GcpSqlDBInstanceSettingsInsights]


@dataclass
class GcpSqlDBInstanceReplicaConfig:
    """
        Attributes:
            ca_certificate: (Optional) PEM representation of the trusted CA's x509 certificate.
            client_certificate: (Optional) PEM representation of the replica's x509 certificate.
            client_key: (Optional) PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate.
            connect_retry_interval: (Optional, Default: 60) The number of seconds between connect retries.
            dump_file_path: (Optional) Path to a SQL file in GCS from which replica instances are created. Format is gs://bucket/filename.
            failover_target: (Optional) Specifies if the replica is the failover target.
            master_heartbeat_period: (Optional) Time in ms between replication heartbeats.
            password: (Optional) Password for the replication connection.
            sslCipher: (Optional) Permissible ciphers for use in SSL encryption.
            username: (Optional) Username for replication connection.
            verify_server_certificate: (Optional) True if the master's common name value is checked during the SSL handshake.
    """
    ca_certificate: Optional[str]
    client_certificate: Optional[str]
    client_key: Optional[str]
    connect_retry_interval: Optional[int]
    dump_file_path: Optional[str]
    failover_target: Optional[bool]
    master_heartbeat_period: Optional[int]
    password: Optional[str]
    sslCipher: Optional[str]
    username: Optional[str]
    verify_server_certificate: Optional[bool]


@dataclass
class GcpSqlDBInstanceRestoreBackupContext:
    """
        Attributes:
            backup_run_id: (Required) The ID of the backup run to restore from.
            instance_id: (Optional) The ID of the instance that the backup was taken from. If left empty, this instance's ID will be used.
            project: (Optional) The full project ID of the source instance.
    """
    backup_run_id: str
    instance_id: Optional[str]
    project: Optional[str]


@dataclass
class GcpSqlDBInstanceClone:
    """
        Attributes:
            source_instance_name: (Required) Name of the source instance which will be cloned.
            point_in_time: (Optional) The timestamp of the point in time that should be restored.
                                      A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
                                      Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
    """
    source_instance_name: str
    point_in_time: Optional[datetime]


class GcpSqlDatabaseInstance(GcpResource):
    """
        Attributes:
            name: (Optional, Computed) The name of this SQL database instance.
            region: (Optional) The region where this instance resides.
            settings: (Optional) The settings used for the sql instance.
            database_version: (Optional, Default: MYSQL_5_6) The version of the sql database.
            master_instance_name: (Optional) The name of the instance that will act as master in replication setup.
            project: (Optional) The ID of the project.
            replica_configuration: (Optional) The configuration for replication. Applicable to MySql instances only.
            root_password: (Optional) The initial root password, applicable to MS Sql instances only.
            encryption_key_name: (Optional) The full path to the encryption key used for the CMEK disk encryption.
            deletion_protection: (Optional, Default: true) The optional setting to whether or not allow Terraform to destroy the instance.
            restore_backup_context: (Optional) The context needed to restore the database to a backup run.
            clone: (Optional) The context needed to create this instance as a clone of another instance.
    """

    def __init__(self,
                 name: str,
                 region: str,
                 settings: Optional[GcpSqlDBInstanceSettings],
                 database_version: Optional[GcpSqlDBInstanceVersion],
                 master_instance_name: str,
                 project: str,
                 replica_configuration: Optional[GcpSqlDBInstanceReplicaConfig],
                 root_password: str,
                 encryption_key_name: str,
                 deletion_protection: bool,
                 restore_backup_context: Optional[GcpSqlDBInstanceRestoreBackupContext],
                 clone: Optional[GcpSqlDBInstanceClone]):

        super().__init__(GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE)
        self.name: Optional[str] = name
        self.region: Optional[str] = region
        self.settings: Optional[GcpSqlDBInstanceSettings] = settings
        self.database_version: Optional[GcpSqlDBInstanceVersion] = database_version
        self.replica_configuration: Optional[GcpSqlDBInstanceReplicaConfig] = replica_configuration
        self.root_password: Optional[str] = root_password
        self.deletion_protection: Optional[bool] = deletion_protection
        self.restore_backup_context: Optional[GcpSqlDBInstanceRestoreBackupContext] = restore_backup_context
        self.clone: Optional[GcpSqlDBInstanceClone] = clone

        # References to other resources
        self.master_instance_name: Optional[str] = master_instance_name
        self.project: str = Optional[project]
        self.encryption_key_name: Optional[str] = encryption_key_name

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

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
