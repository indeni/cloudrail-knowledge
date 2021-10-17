from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDBInstanceSettingsDBFlags, \
    GcpSqlDBInstanceType, GcpSqlDBInstanceVersion, GcpSqlDBInstanceSettingsLocPref, GcpSqlDBInstanceSettingsMaintWindow, \
    GcpSqlDBInstanceSettingsInsights, GcpSqlDBInstanceSettings, GcpSqlDBInstanceSettingsBackupRetention, \
    GcpSqlDBInstanceSettingsBackupConfig, GcpSqlDBInstanceSettingsIPConfig, GcpSqlDBInstanceIPConfigAuthNetworks, \
    GcpSqlDBInstanceReplicaConfig, GcpSqlDBInstanceRestoreBackupContext, GcpSqlDBInstanceClone, GcpSqlDatabaseInstance

from datetime import datetime


class SqlDatabaseInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'sqladmin-v1beta4-instances-list.json'

    def do_build(self, attributes: dict) -> GcpSqlDatabaseInstance:
        instance_type = attributes.get("instanceType")
        if instance_type == GcpSqlDBInstanceType.CLOUD_SQL_INSTANCE.value or \
                instance_type == GcpSqlDBInstanceType.READ_REPLICA_INSTANCE.value:
            settings = self.build_settings_block(attributes)
            database_version = GcpSqlDBInstanceVersion(attributes["databaseVersion"])
            replica_configuration = self.build_replica_configuration(attributes)

            return GcpSqlDatabaseInstance(name=attributes["name"],
                                          region=attributes["region"],
                                          settings=settings,
                                          database_version=database_version,
                                          replica_configuration=replica_configuration,
                                          root_password=attributes.get("rootPassword"),
                                          deletion_protection=None,
                                          restore_backup_context=None,
                                          clone=None,
                                          master_instance_name=attributes.get("masterInstanceName"),
                                          project=attributes["project"],
                                          encryption_key_name=attributes.get("diskEncryptionConfiguration", {}).get("kmsKeyName"))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE

    def build_settings_block(self, attributes: dict):
        if settings := attributes.get("settings"):
            tier = settings.get("tier")
            activation_policy = settings.get("activationPolicy")
            authorized_gae_applications = settings.get("authorizedGaeApplications")
            availability_type = settings.get("availabilityType")
            collation = settings.get("collation")
            crash_safe_replication = settings.get("crashSafeReplicationEnabled")
            disk_autoresize = None
            disk_size = None
            disk_type = settings.get("dataDiskType")
            pricing_plan = settings.get("pricingPlan")
            replication_type = settings.get("replicationType")
            user_labels = settings.get("userLabels")
            database_flags_list = settings.get("databaseFlags")
            database_flags = [GcpSqlDBInstanceSettingsDBFlags(database_flag["name"], database_flag["value"])
                              for database_flag in database_flags_list] if database_flags_list else None
            backup_configuration = self.build_backup_configuration(settings)
            ip_configuration = self.build_ip_configuration(settings)
            location_preference = settings.get("locationPreference")
            location_preference = GcpSqlDBInstanceSettingsLocPref(location_preference.get("followGaeApplication"),
                                                                  location_preference.get("zone")) if location_preference else None
            maintenance_window = settings.get("maintenanceWindow")
            maintenance_window = GcpSqlDBInstanceSettingsMaintWindow(maintenance_window.get("day"),
                                                                     maintenance_window.get("hour"),
                                                                     maintenance_window.get("updateTrack")) if maintenance_window else None
            insights_config = settings.get("insightsConfig")
            insights_config = GcpSqlDBInstanceSettingsInsights(insights_config.get("queryInsightsEnabled"),
                                                               insights_config.get("queryStringLength"),
                                                               insights_config.get("recordApplicationTags"),
                                                               insights_config.get("recordClientAddress")) if insights_config else None

            return GcpSqlDBInstanceSettings(tier, activation_policy, authorized_gae_applications, crash_safe_replication,
                                            availability_type, collation, disk_autoresize,
                                            disk_size, disk_type, pricing_plan, replication_type,
                                            user_labels, database_flags, backup_configuration, ip_configuration, location_preference,
                                            maintenance_window, insights_config)

        return None

    def build_backup_configuration(self, settings: dict):
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

    def build_authorized_network(self, authorized_network: dict) -> GcpSqlDBInstanceIPConfigAuthNetworks:
        expiration_time = None
        if expiration_time_str := authorized_network.get("expirationTime"):
            expiration_time_str_list = expiration_time_str.split(".")
            expiration_time_str = expiration_time_str_list.split[0] if len(expiration_time_str_list) > 1 else expiration_time_str_list.split[0][:-1]
            expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%dT%H:%M:%S')

        return GcpSqlDBInstanceIPConfigAuthNetworks(expiration_time,
                                                    authorized_network.get("name"),
                                                    authorized_network.get("value"))

    def build_replica_configuration(self, attributes: dict):
        if replica_configuration := attributes.get("replicaConfiguration"):
            if mysql_replica_configuration := replica_configuration.get("mysqlReplicaConfiguration"):
                ca_certificate = mysql_replica_configuration.get("caCertificate")
                client_certificate = mysql_replica_configuration.get("clientCertificate")
                client_key = mysql_replica_configuration.get("clientKey")
                connect_retry_interval = mysql_replica_configuration.get("connectRetryInterval")
                dump_file_path = mysql_replica_configuration.get("dumpFilePath")
                failover_target = replica_configuration.get("caCertificate")
                master_heartbeat_period = mysql_replica_configuration.get("masterHeartbeatPeriod")
                password = mysql_replica_configuration.get("password")
                sslCipher = mysql_replica_configuration.get("sslCipher")
                username = mysql_replica_configuration.get("username")
                verify_server_certificate = mysql_replica_configuration.get("verifyServerCertificate")

                return GcpSqlDBInstanceReplicaConfig(ca_certificate, client_certificate, client_key, connect_retry_interval, dump_file_path,
                                                     failover_target, master_heartbeat_period, password, sslCipher, username, verify_server_certificate)

        return None

    def build_restore_backup_context(self, attributes: dict):
        if restore_backup_context := attributes.get("restore_backup_context"):
            backup_run_id = restore_backup_context["backup_run_id"]
            instance_id = restore_backup_context.get("instance_id")
            project = restore_backup_context.get("project")

            return GcpSqlDBInstanceRestoreBackupContext(backup_run_id, instance_id, project)

        return None

    def build_clone(self, attributes: dict):
        if clone := attributes.get("cloneContext"):
            source_instance_name = clone["source_instance_name"]
            point_in_time = None
            if point_in_time_str := clone.get("pointInTime"):
                point_in_time_str_list = point_in_time_str.split(".")
                point_in_time_str = point_in_time_str_list.split[0] if len(point_in_time_str_list) > 1 else point_in_time_str_list.split[0][:-1]
                point_in_time = datetime.strptime(point_in_time_str, '%Y-%m-%dT%H:%M:%S')

            return GcpSqlDBInstanceClone(source_instance_name, point_in_time)

        return None
