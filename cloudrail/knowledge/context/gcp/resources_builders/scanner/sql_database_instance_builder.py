# pylint: disable=consider-using-in
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDBInstanceType, GcpSqlDBInstanceVersion, GcpSqlDBInstanceSettingsDBFlags, \
    GcpSqlDBInstanceSettingsBackupRetention, GcpSqlDBInstanceSettingsBackupConfig, GcpSqlDBInstanceIPConfigAuthNetworks, GcpSqlDBInstanceSettingsIPConfig, \
    GcpSqlDatabaseInstance, GcpSqlDBInstanceSettings
from cloudrail.knowledge.utils.tags_utils import get_gcp_labels
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

            sql_instance = GcpSqlDatabaseInstance(name=attributes["name"],
                                                  region=attributes["region"],
                                                  settings=settings,
                                                  database_version=database_version)
            if sql_instance.settings:
                sql_instance.labels = get_gcp_labels(attributes['settings'].get('userLabels'), attributes['salt'])
            return sql_instance

        return None

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
        backup_configuration = settings.get("backupConfiguration", {})
        binary_log_enabled = backup_configuration.get("binaryLogEnabled", False)
        enabled = backup_configuration.get("enabled")
        start_time_str = backup_configuration.get("startTime")
        start_time = datetime.strptime(start_time_str, "%H:%M") if start_time_str else None
        point_in_time_recovery_enabled = backup_configuration.get("pointInTimeRecoveryEnabled", False)
        location = backup_configuration.get("location")
        transaction_log_retention_days = backup_configuration.get("transactionLogRetentionDays")
        backup_retention_settings_dict = backup_configuration.get("backupRetentionSettings", {})
        backup_retention_settings = GcpSqlDBInstanceSettingsBackupRetention(backup_retention_settings_dict.get("retainedBackups"),
                                                                            backup_retention_settings_dict.get("retentionUnit"))

        return GcpSqlDBInstanceSettingsBackupConfig(binary_log_enabled, enabled, start_time, point_in_time_recovery_enabled,
                                                    location, transaction_log_retention_days, backup_retention_settings)

    def build_ip_configuration(self, settings: dict):
        ip_configuration = settings.get("ipConfiguration", {})
        ipv4_enabled = ip_configuration.get("ipv4Enabled")
        private_network = ip_configuration.get("privateNetwork")
        require_ssl = ip_configuration.get("requireSsl", False)
        authorized_networks_list = ip_configuration.get("authorizedNetworks", [])
        authorized_networks = [self.build_authorized_network(authorized_network)
                               for authorized_network in authorized_networks_list]

        return GcpSqlDBInstanceSettingsIPConfig(ipv4_enabled, private_network, require_ssl, authorized_networks)

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
