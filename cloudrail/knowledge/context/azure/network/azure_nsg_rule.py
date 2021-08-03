from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.aws_connection import ConnectionDirectionType
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_set import PortSet


class NetworkSecurityRuleActionType(str, Enum):
    ALLOW = 'Allow'
    DENY = 'Deny'


class AzureNetworkSecurityRule(AzureResource):
    """
        Attributes:
            name: The NSG name.
            priority: The rule's priority. The lower the number, the higher priority.
            direction: The rule direction. Either inbound or outbound.
            access: The rule's access type. Either Allow or Deny.
            protocol: The IpProtocol this rule affects. For example, TCP, UDP, etc.
            destination_port_ranges: The set of ports this rule addresses.
            source_address_prefixes: The addresses of the source. These can be CIDR blocks, VirtualNetwork/AzureLoadBalancer/Internet/* or a service tags.
            destination_address_prefixes: The addresses of the destination. These can be CIDR blocks, VirtualNetwork/AzureLoadBalancer/Internet/* or a service tags.
            network_security_group_name: The NSG name this rule is assigned to.
    """

    def get_keys(self) -> List[str]:
        return [self.network_security_group_name, self.priority]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass  # TOOD

    @property
    def is_tagable(self) -> bool:
        return False

    def __init__(self,
                 name: str,
                 priority: int,
                 direction: ConnectionDirectionType,
                 access: NetworkSecurityRuleActionType,
                 protocol: IpProtocol,
                 destination_port_ranges: PortSet,
                 source_address_prefixes: List[str],
                 destination_address_prefixes: List[str],
                 network_security_group_name: str
                 ):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name
        self.priority: int = priority
        self.direction: ConnectionDirectionType = direction
        self.access: NetworkSecurityRuleActionType = access
        self.protocol: IpProtocol = protocol
        self.destination_port_ranges: PortSet = destination_port_ranges
        # read the docs as this can contain an enum as well, (Optional) CIDR or source IP range or * to match any IP. Tags such as ‘VirtualNetwork’, ‘AzureLoadBalancer’ and ‘Internet’ can also be used
        self.source_address_prefixes: List[str] = source_address_prefixes
        # same shit as source
        self.destination_address_prefixes: List[str] = destination_address_prefixes
        self.network_security_group_name: str = network_security_group_name

    @staticmethod
    def is_standalone() -> bool:
        return False
