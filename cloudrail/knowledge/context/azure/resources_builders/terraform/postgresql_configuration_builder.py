from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AzurePostgreSqlServerConfigurationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzurePostgreSqlServerConfiguration:
        return AzurePostgreSqlServerConfiguration(server_name=attributes['server_name'],
                                                  name=attributes['name'],
                                                  value=attributes['value'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_POSTGRESQL_SERVER_CONFIGURATION
