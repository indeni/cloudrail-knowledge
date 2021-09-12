from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.network.azure_vnet_gateway import AzureVirtualNetworkGateway, VirtualNetworkGatewayType


class VnetGatewayBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'virtual-network-gateways.json'

    def do_build(self, attributes: dict) -> AzureVirtualNetworkGateway:
        return AzureVirtualNetworkGateway(name=attributes['name'],
                                          gateway_type=VirtualNetworkGatewayType(attributes['properties']['gatewayType']),
                                          sku_tier=attributes['properties']['sku']['tier'])
