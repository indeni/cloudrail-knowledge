import ipaddress

from cloudrail.knowledge.context.azure.resources.network.azure_virtual_network import AzureVirtualNetwork
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class VirtualNetworkBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-virtual-networks.json'

    def do_build(self, attributes: dict) -> AzureVirtualNetwork:
        return AzureVirtualNetwork(network_name=attributes['name'],
                                   cidr_addresses=[ipaddress.ip_network(cidr)
                                                   for cidr in attributes['properties']['addressSpace']['addressPrefixes']])
