import ipaddress
from cloudrail.knowledge.context.azure.resources.network.azure_virtual_network import AzureVirtualNetwork
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class VirtualNetworkBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-virtual-networks.json'

    def do_build(self, attributes: dict) -> AzureVirtualNetwork:
        bgp_community = None
        if bgp := attributes['properties'].get('bgpCommunities'):
            bgp_community = f"{bgp['regionalCommunity']}:{bgp['virtualNetworkCommunity']}"
        dns_servers = []
        if dhcp_opt := attributes['properties'].get('dhcpOptions'):
            dns_servers = dhcp_opt.get('dnsServers')
        flow_timeout_in_minutes: int = int(attributes['properties'].get('flowTimeoutInMinutes', -1))
        return AzureVirtualNetwork(network_name=attributes['name'],
                                   cidr_addresses=[ipaddress.ip_network(cidr)
                                                   for cidr in attributes['properties']['addressSpace']['addressPrefixes']],
                                   bgp_community=bgp_community,
                                   dns_servers=dns_servers,
                                   flow_timeout_in_minutes=flow_timeout_in_minutes)
