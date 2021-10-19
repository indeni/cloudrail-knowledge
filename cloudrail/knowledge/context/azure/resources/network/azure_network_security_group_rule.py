from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.connection import ConnectionDirectionType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
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
            source_application_security_group_ids: The application security group id of the source that this rule addresses.
            destination_application_security_group_ids: The application security group id of the destination that this rule addresses.
    """
    def __init__(self,
                 name: str,
                 priority: int,
                 direction: ConnectionDirectionType,
                 access: NetworkSecurityRuleActionType,
                 protocol: IpProtocol,
                 destination_port_ranges: PortSet,
                 source_address_prefixes: List[str],
                 destination_address_prefixes: List[str],
                 network_security_group_name: str,
                 source_application_security_group_ids: List[str],
                 destination_application_security_group_ids: List[str]
                 ):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name
        self.priority: int = priority
        self.direction: ConnectionDirectionType = direction
        self.access: NetworkSecurityRuleActionType = access
        self.protocol: IpProtocol = protocol
        self.destination_port_ranges: PortSet = destination_port_ranges
        self.source_address_prefixes: List[str] = source_address_prefixes
        self.destination_address_prefixes: List[str] = destination_address_prefixes
        self.network_security_group_name: str = network_security_group_name
        self.source_application_security_group_ids: List[str] = source_application_security_group_ids
        self.destination_application_security_group_ids: List[str] = destination_application_security_group_ids

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Network/networkSecurityGroups/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'priority': self.priority,
                'direction': self.direction.value,
                'access': self.access.value,
                'protocol': str(self.protocol),
                'destination_port_ranges': str(self.destination_port_ranges),
                'source_address_prefixes': self.source_address_prefixes,
                'destination_address_prefixes': self.destination_address_prefixes,
                'network_security_group_name': self.network_security_group_name,
                'source_application_security_group_ids': self.source_application_security_group_ids,
                'destination_application_security_group_ids': self.destination_application_security_group_ids}
