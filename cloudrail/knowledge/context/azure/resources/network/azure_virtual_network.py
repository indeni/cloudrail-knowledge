import ipaddress
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureVirtualNetwork(AzureResource):

    """
        Attributes:
            network_name: virtual network name
            cidr_addresses: virtual network possible cidr addresses
            subnets: virtual network subnets
            bgp_community: The BGP community attribute.
            dns_servers: List of IP addresses of DNS servers.
            flow_timeout_in_minutes: The flow timeout in minutes for the Virtual Network. Used to enable connection tracking for intra-VM flows.
    """
    def __init__(self, network_name: str, cidr_addresses: List[ipaddress.IPv4Network],
                 bgp_community: str, dns_servers: List[str], flow_timeout_in_minutes: int):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_NETWORK)
        self.network_name: str = network_name
        self.cidr_addresses: List[ipaddress.IPv4Network] = cidr_addresses
        self.bgp_community: str = bgp_community
        self.dns_servers: List[str] = dns_servers
        self.flow_timeout_in_minutes: int = flow_timeout_in_minutes
        self.subnets: AliasesDict[AzureSubnet] = AliasesDict()

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}' \
               f'/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Network/virtualNetworks/{self.network_name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {
            'cidr_addresses': [str(cidr) for cidr in self.cidr_addresses],
            'subnets': [subnet.to_drift_detection_object() for subnet in self.subnets.values()],
            'tags': self.tags
        }

    def get_name(self) -> Optional[str]:
        return self.network_name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Virtual Network' + ('s' if is_plural else '')
