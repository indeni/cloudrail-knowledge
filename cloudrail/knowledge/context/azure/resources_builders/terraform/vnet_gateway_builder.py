from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_vnet_gateway import AzureVirtualNetworkGateway, VirtualNetworkGatewayType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VnetGatewayBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualNetworkGateway:
        return AzureVirtualNetworkGateway(name=attributes['name'],
                                          gateway_type=VirtualNetworkGatewayType(attributes['type']),
                                          sku_tier=attributes['sku'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_NETWORK_GATEWAY
