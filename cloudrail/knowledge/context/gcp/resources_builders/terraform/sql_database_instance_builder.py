from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import *
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDBInstanceSettingsDBFlags

from datetime import datetime


class SqlDatabaseInstanceBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpSqlDatabaseInstance:
        settings = self.build_settings_block(attributes)
        database_version = GcpSqlDBInstanceVersion(attributes.get("database_version", "MYSQL_5_6"))
        replica_configuration = self.build_replica_configuration(attributes)
        restore_backup_context = self.build_restore_backup_context(attributes)
        clone = self.build_clone(attributes)

        return GcpSqlDatabaseInstance(name=attributes.get("name"),
                                      region=attributes.get("region"),
                                      settings=settings,
                                      database_version=database_version,
                                      replica_configuration=replica_configuration,
                                      root_password=attributes.get("root_password"),
                                      deletion_protection=attributes.get("deletion_protection", True),
                                      restore_backup_context=restore_backup_context,
                                      clone=clone,
                                      master_instance_name=attributes.get("master_instance_name"),
                                      project=attributes.get("project"),
                                      encryption_key_name=attributes.get("encryption_key_name"))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE

    def build_settings_block(self, attributes: dict):
        settings_block = self._get_known_value(attributes, "settings")
        settings = settings_block[0] if settings_block else None

        if settings:
            tier = settings.get("tier", None)
            activation_policy = self._get_known_value(settings, "activation_policy")
            authorized_gae_applications = self._get_known_value(settings, "authorized_gae_applications")
            availability_type = self._get_known_value(settings, "availability_type")
            collation = self._get_known_value(settings, "collation")
            crash_safe_replication = self._get_known_value(settings, "crash_safe_replication")
            disk_autoresize = self._get_known_value(settings, "disk_autoresize", True)
            disk_size = self._get_known_value(settings, "disk_size", 10)
            disk_type = self._get_known_value(settings, "disk_type", "PD_SSD")
            pricing_plan = self._get_known_value(settings, "pricing_plan")
            replication_type = self._get_known_value(settings, "replication_type")
            user_labels = self._get_known_value(settings, "user_labels")
            database_flags_list = self._get_known_value(settings, "database_flags")
            database_flags = [GcpSqlDBInstanceSettingsDBFlags(database_flag["name"], database_flag["value"])
                              for database_flag in database_flags_list] if database_flags_list else None
            backup_configuration = self.build_backup_configuration(settings)
            ip_configuration = self.build_ip_configuration(settings)
            location_preference_block = self._get_known_value(settings, "location_preference")
            location_preference = location_preference_block[0] if location_preference_block else None
            location_preference = GcpSqlDBInstanceSettingsLocPref(location_preference.get("follow_gae_application"),
                                                                  location_preference.get("zone")) if location_preference else None
            maintenance_window_block = self._get_known_value(settings, "maintenance_window")
            maintenance_window = maintenance_window_block[0] if maintenance_window_block else None
            maintenance_window = GcpSqlDBInstanceSettingsMaintWindow(maintenance_window.get("day"),
                                                                     maintenance_window.get("hour"),
                                                                     maintenance_window.get("update_track")) if maintenance_window else None
            insights_config_block = self._get_known_value(settings, "insights_config")
            insights_config = insights_config_block[0] if insights_config_block else None
            insights_config = GcpSqlDBInstanceSettingsInsights(insights_config.get("query_insights_enabled", None),
                                                               insights_config.get("query_string_length", 1024),
                                                               insights_config.get("record_application_tags", None),
                                                               insights_config.get("record_client_address", None)) if insights_config else None

            return GcpSqlDBInstanceSettings(tier, activation_policy, authorized_gae_applications, crash_safe_replication,
                                            availability_type, collation, disk_autoresize,
                                            disk_size, disk_type, pricing_plan, replication_type,
                                            user_labels, database_flags, backup_configuration, ip_configuration, location_preference,
                                            maintenance_window, insights_config)

        return None

    def build_backup_configuration(self, settings: dict):
        backup_configuration_block = self._get_known_value(settings, "backup_configuration")
        backup_configuration = backup_configuration_block[0] if backup_configuration_block else None

        if backup_configuration:
            binary_log_enabled = self._get_known_value(backup_configuration, "binary_log_enabled")
            enabled = self._get_known_value(backup_configuration, "enabled")
            start_time_str = self._get_known_value(backup_configuration, "start_time")
            start_time = datetime.strptime(start_time_str, "%H:%M") if start_time_str else None
            point_in_time_recovery_enabled = self._get_known_value(backup_configuration, "point_in_time_recovery_enabled")
            location = self._get_known_value(backup_configuration, "location")
            transaction_log_retention_days = self._get_known_value(backup_configuration, "transaction_log_retention_days")
            backup_retention_settings_block = self._get_known_value(backup_configuration, "backup_retention_settings")
            backup_retention_settings = GcpSqlDBInstanceSettingsBackupRetention(backup_retention_settings_block[0]["retained_backups"],
                                                                                backup_retention_settings_block[0].get("retention_unit", "COUNT")) if backup_retention_settings_block else None

            return GcpSqlDBInstanceSettingsBackupConfig(binary_log_enabled, enabled, start_time, point_in_time_recovery_enabled,
                                                        location, transaction_log_retention_days, backup_retention_settings)
        return None

    def build_ip_configuration(self, settings: dict):
        ip_configuration_block = self._get_known_value(settings, "ip_configuration")
        ip_configuration = ip_configuration_block[0] if ip_configuration_block else None

        if ip_configuration:
            ipv4_enabled = self._get_known_value(ip_configuration, "ipv4_enabled")
            private_network = ip_configuration.get("private_network")
            require_ssl = self._get_known_value(ip_configuration, "require_ssl")
            authorized_networks_list = self._get_known_value(ip_configuration, "authorized_networks")
            authorized_networks = [self.build_authorized_network(authorized_network)
                                   for authorized_network in authorized_networks_list] if authorized_networks_list else None

            return GcpSqlDBInstanceSettingsIPConfig(ipv4_enabled, private_network, require_ssl, authorized_networks)

        return None

    def build_authorized_network(self, authorized_network: dict) -> GcpSqlDBInstanceIPConfigAuthNetworks:
        expiration_time = None
        if expiration_time_str := self._get_known_value(authorized_network, "expiration_time"):
            expiration_time_str_list = expiration_time_str.split(".")
            expiration_time_str = expiration_time_str_list.split[0] if len(expiration_time_str_list) > 1 else expiration_time_str_list.split[0][:-1]
            expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%dT%H:%M:%S')

        return GcpSqlDBInstanceIPConfigAuthNetworks(expiration_time,
                                                    self._get_known_value(authorized_network, "name"),
                                                    authorized_network["value"])

    def build_replica_configuration(self, attributes: dict):
        replica_configuration_block = self._get_known_value(attributes, "replica_configuration")
        replica_configuration = replica_configuration_block[0] if replica_configuration_block else None

        if replica_configuration:
            ca_certificate = self._get_known_value(replica_configuration, "ca_certificate")
            client_certificate = self._get_known_value(replica_configuration, "client_certificate")
            client_key = self._get_known_value(replica_configuration, "client_key")
            connect_retry_interval = self._get_known_value(replica_configuration, "connect_retry_interval", 60)
            dump_file_path = self._get_known_value(replica_configuration, "dump_file_path")
            failover_target = self._get_known_value(replica_configuration, "failover_target")
            master_heartbeat_period = self._get_known_value(replica_configuration, "master_heartbeat_period")
            password = self._get_known_value(replica_configuration, "password")
            sslCipher = self._get_known_value(replica_configuration, "sslCipher")
            username = self._get_known_value(replica_configuration, "username")
            verify_server_certificate = self._get_known_value(replica_configuration, "verify_server_certificate")

            return GcpSqlDBInstanceReplicaConfig(ca_certificate, client_certificate, client_key, connect_retry_interval, dump_file_path,
                                                 failover_target, master_heartbeat_period, password, sslCipher, username, verify_server_certificate)

        return None

    def build_restore_backup_context(self, attributes: dict):
        restore_backup_context_block = self._get_known_value(attributes, "restore_backup_context")
        restore_backup_context = restore_backup_context_block[0] if restore_backup_context_block else None

        if restore_backup_context:
            backup_run_id = restore_backup_context["backup_run_id"]
            instance_id = restore_backup_context.get("instance_id")
            project = restore_backup_context.get("project")

            return GcpSqlDBInstanceRestoreBackupContext(backup_run_id, instance_id, project)

        return None

    def build_clone(self, attributes: dict):
        clone_block = self._get_known_value(attributes, "clone")
        clone = clone_block[0] if clone_block else None

        if clone:
            source_instance_name = clone["source_instance_name"]
            point_in_time = None
            if point_in_time_str := clone.get("point_in_time"):
                point_in_time_str_list = point_in_time_str.split(".")
                point_in_time_str = point_in_time_str_list.split[0] if len(point_in_time_str_list) > 1 else point_in_time_str_list.split[0][:-1]
                point_in_time = datetime.strptime(point_in_time_str, '%Y-%m-%dT%H:%M:%S')

            return GcpSqlDBInstanceClone(source_instance_name, point_in_time)

        return None
