from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SubnetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSubnet:
        return AzureSubnet(name=attributes['name'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SUBNET
