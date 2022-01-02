from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer, \
    PostgreSqlServerVersion, PostgreSqlServerIdentity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class PostgreSqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'postgresql-servers-list.json'

    def do_build(self, attributes: dict) -> AzurePostgreSqlServer:
        identity_type = None
        if identity := attributes.get('identity'):
            identity_type = PostgreSqlServerIdentity(identity['type'])
        properties = attributes['properties']
        return AzurePostgreSqlServer(server_name=attributes['name'],
                                     ssl_enforcement_enabled=properties['sslEnforcement'] == 'Enabled',
                                     sku_name=attributes['sku']['name'],
                                     version=PostgreSqlServerVersion(properties['version']),
                                     administrator_login=properties.get('administratorLogin'),
                                     auto_grow_enabled=properties.get('storageProfile').get('storageAutogrow') == 'Enabled',
                                     backup_retention_days=properties.get('storageProfile').get('backupRetentionDays'),
                                     geo_redundant_backup_enabled=properties.get('storageProfile').get('geoRedundantBackup') == 'Enabled',
                                     identity=identity_type,
                                     infrastructure_encryption_enabled=properties.get('infrastructureEncryption') == 'Enabled',
                                     public_network_access_enabled=properties.get('publicNetworkAccess') == 'Enabled',
                                     ssl_minimal_tls_version_enforced=properties.get('minimalTlsVersion', 'TLSEnforcementDisabled'),
                                     storage_mb=properties.get('storageProfile').get('storageMB'))
