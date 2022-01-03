import ipaddress
from typing import List
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet


class SubnetsBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'subnets.json'

    def do_build(self, attributes: dict) -> AzureSubnet:
        cidr_addresses: List[ipaddress.IPv4Network] = [ipaddress.ip_network(attributes['properties']['addressPrefix'])] \
            if attributes['properties'].get('addressPrefix') \
            else [ipaddress.ip_network(cidr) for cidr in attributes['properties']['addressSpace']['addressPrefixes']]
        return AzureSubnet(name=attributes['name'],
                           network_name=attributes['id'].split('/')[-3],
                           cidr_addresses=cidr_addresses)
