from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_database_configuration import AzureDatabaseConfiguration

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class PostgreSqlServerConfigurationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureDatabaseConfiguration:
        return AzureDatabaseConfiguration(name=attributes['name'],
                                          value=attributes['value'],
                                          server_name=attributes['server_name'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_POSTGRESQL_CONFIGURATION
