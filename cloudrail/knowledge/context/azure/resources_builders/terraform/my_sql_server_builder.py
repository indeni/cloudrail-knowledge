from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mysql_server import AzureMySqlServer

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class MySqlServerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureMySqlServer:
        return AzureMySqlServer(server_name=attributes['name'],
                                ssl_enforcement_enabled=attributes['ssl_enforcement_enabled'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MYSQL_SERVER
