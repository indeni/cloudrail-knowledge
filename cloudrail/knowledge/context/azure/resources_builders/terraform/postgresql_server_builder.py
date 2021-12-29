from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer, \
    PostgreSqlServerVersion, PostgreSqlServerIdentity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class PostgreSqlServerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzurePostgreSqlServer:
        identity_type = None
        if identity := attributes['identity']:
            identity_type = PostgreSqlServerIdentity(identity[0]['type'])
        return AzurePostgreSqlServer(server_name=attributes['name'],
                                     ssl_enforcement_enabled=attributes['ssl_enforcement_enabled'],
                                     sku_name=attributes['sku_name'],
                                     version=PostgreSqlServerVersion(attributes['version']),
                                     administrator_login=self._get_known_value(attributes, 'administrator_login'),
                                     auto_grow_enabled=self._get_known_value(attributes, 'auto_grow_enabled', True),
                                     backup_retention_days=self._get_known_value(attributes, 'backup_retention_days'),
                                     geo_redundant_backup_enabled=self._get_known_value(attributes, 'geo_redundant_backup_enabled'),
                                     identity=identity_type,
                                     infrastructure_encryption_enabled=self._get_known_value(attributes, 'infrastructure_encryption_enabled', False),
                                     public_network_access_enabled=self._get_known_value(attributes, 'public_network_access_enabled', True),
                                     ssl_minimal_tls_version_enforced=self._get_known_value(attributes, 'ssl_minimal_tls_version_enforced', 'TLSEnforcementDisabled'),
                                     storage_mb=self._get_known_value(attributes, 'storage_mb'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_POSTGRESQL_SERVER
