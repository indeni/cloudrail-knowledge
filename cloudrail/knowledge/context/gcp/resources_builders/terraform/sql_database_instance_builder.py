from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDBInstanceVersion, GcpSqlDBInstanceSettingsDBFlags, GcpSqlDBInstanceSettingsBackupRetention, \
    GcpSqlDBInstanceSettingsBackupConfig, GcpSqlDBInstanceIPConfigAuthNetworks, GcpSqlDBInstanceSettingsIPConfig, GcpSqlDBInstanceSettings, GcpSqlDatabaseInstance
from cloudrail.knowledge.utils.datetime_util import build_datetime


class SqlDatabaseInstanceBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpSqlDatabaseInstance:
        settings = self.build_settings_block(attributes)
        database_version = GcpSqlDBInstanceVersion(attributes.get("database_version", "MYSQL_5_6"))

        sql_instance = GcpSqlDatabaseInstance(name=attributes.get("name"),
                                              region=attributes.get("region"),
                                              settings=settings,
                                              database_version=database_version)
        if sql_instance.settings:
            sql_instance.labels = self._get_known_value(attributes['settings'][0], 'user_labels')
        return sql_instance

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE

    def build_settings_block(self, attributes: dict):
        settings_block = self._get_known_value(attributes, "settings")
        settings = settings_block[0] if settings_block else None

        if settings:
            tier = settings.get("tier", None)
            database_flags_list = self._get_known_value(settings, "database_flags")
            database_flags = [GcpSqlDBInstanceSettingsDBFlags(database_flag["name"], database_flag["value"])
                              for database_flag in database_flags_list] if database_flags_list else None
            backup_configuration = self.build_backup_configuration(settings)
            ip_configuration = self.build_ip_configuration(settings)

            return GcpSqlDBInstanceSettings(tier, database_flags, backup_configuration, ip_configuration)

        return None

    def build_backup_configuration(self, settings: dict):
        backup_configuration_block = self._get_known_value(settings, "backup_configuration", [])
        backup_configuration = backup_configuration_block[0] if backup_configuration_block else {}

        binary_log_enabled = self._get_known_value(backup_configuration, "binary_log_enabled", False)
        enabled = self._get_known_value(backup_configuration, "enabled", False)
        start_time_str = self._get_known_value(backup_configuration, "start_time", "16:00")
        start_time = build_datetime(start_time_str, "%H:%M")
        point_in_time_recovery_enabled = self._get_known_value(backup_configuration, "point_in_time_recovery_enabled", False)
        location = self._get_known_value(backup_configuration, "location")
        transaction_log_retention_days = self._get_known_value(backup_configuration, "transaction_log_retention_days", 7)
        backup_retention_settings_block = self._get_known_value(backup_configuration, "backup_retention_settings", [{}])
        backup_retention_settings = GcpSqlDBInstanceSettingsBackupRetention(backup_retention_settings_block[0].get("retained_backups", 7),
                                                                            backup_retention_settings_block[0].get("retention_unit", "COUNT"))

        return GcpSqlDBInstanceSettingsBackupConfig(binary_log_enabled, enabled, start_time, point_in_time_recovery_enabled,
                                                    location, transaction_log_retention_days, backup_retention_settings)

    def build_ip_configuration(self, settings: dict):
        ip_configuration_block = self._get_known_value(settings, "ip_configuration", [])
        ip_configuration = ip_configuration_block[0] if ip_configuration_block else {}

        ipv4_enabled = self._get_known_value(ip_configuration, "ipv4_enabled", True)
        private_network = self._get_known_value(ip_configuration, "private_network")
        require_ssl = self._get_known_value(ip_configuration, "require_ssl", False)
        authorized_networks_list = self._get_known_value(ip_configuration, "authorized_networks")
        authorized_networks = [self.build_authorized_network(authorized_network)
                               for authorized_network in authorized_networks_list] if authorized_networks_list else []

        return GcpSqlDBInstanceSettingsIPConfig(ipv4_enabled, private_network, require_ssl, authorized_networks)

    def build_authorized_network(self, authorized_network: dict) -> GcpSqlDBInstanceIPConfigAuthNetworks:
        expiration_time = None
        if expiration_time_str := self._get_known_value(authorized_network, "expiration_time"):
            expiration_time_str_list = expiration_time_str.split(".")
            expiration_time_str = expiration_time_str_list[0] if len(expiration_time_str_list) > 1 else expiration_time_str_list[0][:-1]
            expiration_time = build_datetime(expiration_time_str, '%Y-%m-%dT%H:%M:%S')

        return GcpSqlDBInstanceIPConfigAuthNetworks(expiration_time,
                                                    self._get_known_value(authorized_network, "name"),
                                                    authorized_network["value"])
