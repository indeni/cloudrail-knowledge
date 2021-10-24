# pylint: disable=consider-using-in
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDBInstanceType, GcpSqlDBInstanceVersion, GcpSqlDBInstanceSettingsDBFlags, \
    GcpSqlDBInstanceSettingsBackupRetention, GcpSqlDBInstanceSettingsBackupConfig, GcpSqlDBInstanceIPConfigAuthNetworks, GcpSqlDBInstanceSettingsIPConfig, \
    GcpSqlDatabaseInstance, GcpSqlDBInstanceSettings

from datetime import datetime


class SqlDatabaseInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'sqladmin-v1beta4-instances-list.json'

    def do_build(self, attributes: dict):
        instance_type = attributes.get("instanceType")
        if instance_type == GcpSqlDBInstanceType.CLOUD_SQL_INSTANCE.value or \
                instance_type == GcpSqlDBInstanceType.READ_REPLICA_INSTANCE.value:
            settings = self.build_settings_block(attributes)
            database_version = GcpSqlDBInstanceVersion(attributes["databaseVersion"])

            return GcpSqlDatabaseInstance(name=attributes["name"],
                                          region=attributes["region"],
                                          settings=settings,
                                          database_version=database_version)

        return None

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE

    def build_settings_block(self, attributes: dict):
        if settings := attributes.get("settings"):
            tier = settings.get("tier")
            database_flags_list = settings.get("databaseFlags")
            database_flags = [GcpSqlDBInstanceSettingsDBFlags(database_flag["name"], database_flag["value"])
                              for database_flag in database_flags_list] if database_flags_list else None
            backup_configuration = self.build_backup_configuration(settings)
            ip_configuration = self.build_ip_configuration(settings)

            return GcpSqlDBInstanceSettings(tier, database_flags, backup_configuration, ip_configuration)

        return None

    @staticmethod
    def build_backup_configuration(settings: dict):
        if backup_configuration := settings.get("backupConfiguration"):
            binary_log_enabled = backup_configuration.get("binaryLogEnabled")
            enabled = backup_configuration.get("enabled")
            start_time_str = backup_configuration.get("startTime")
            start_time = datetime.strptime(start_time_str, "%H:%M") if start_time_str else None
            point_in_time_recovery_enabled = backup_configuration.get("pointInTimeRecoveryEnabled")
            location = backup_configuration.get("location")
            transaction_log_retention_days = backup_configuration.get("transactionLogRetentionDays")
            backup_retention_settings = backup_configuration.get("backupRetentionSettings")
            backup_retention_settings = GcpSqlDBInstanceSettingsBackupRetention(backup_retention_settings.get("retainedBackups"),
                                                                                backup_retention_settings.get("retentionUnit")) if backup_retention_settings else None

            return GcpSqlDBInstanceSettingsBackupConfig(binary_log_enabled, enabled, start_time, point_in_time_recovery_enabled,
                                                        location, transaction_log_retention_days, backup_retention_settings)
        return None

    def build_ip_configuration(self, settings: dict):
        if ip_configuration := settings.get("ipConfiguration"):
            ipv4_enabled = ip_configuration.get("ipv4Enabled")
            private_network = ip_configuration.get("privateNetwork")
            require_ssl = ip_configuration.get("requireSsl")
            authorized_networks_list = ip_configuration.get("authorizedNetworks")
            authorized_networks = [self.build_authorized_network(authorized_network)
                                   for authorized_network in authorized_networks_list] if authorized_networks_list else None

            return GcpSqlDBInstanceSettingsIPConfig(ipv4_enabled, private_network, require_ssl, authorized_networks)

        return None

    @staticmethod
    def build_authorized_network(authorized_network: dict) -> GcpSqlDBInstanceIPConfigAuthNetworks:
        expiration_time = None
        if expiration_time_str := authorized_network.get("expirationTime"):
            expiration_time_str_list = expiration_time_str.split(".")
            expiration_time_str = expiration_time_str_list[0] if len(expiration_time_str_list) > 1 else expiration_time_str_list[0][:-1]
            expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%dT%H:%M:%S')

        return GcpSqlDBInstanceIPConfigAuthNetworks(expiration_time,
                                                    authorized_network.get("name"),
                                                    authorized_network.get("value"))
