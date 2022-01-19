import ipaddress
from typing import List, Optional
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup


class AzureSubnet(AzureResource):
    """
        Attributes:
            name: The name of this subnet
            network_name: virtual network name associated with this subnet
            cidr_addresses: subnet cidr addresses
            network_security_group: The actual security group that's attached to this subnet.
    """

    def __init__(self, name: str, network_name: str, cidr_addresses: List[ipaddress.IPv4Network]):
        super().__init__(AzureResourceType.AZURERM_SUBNET)
        self.name: str = name
        self.network_name: str = network_name
        self.cidr_addresses: List[ipaddress.IPv4Network] = cidr_addresses
        self.network_security_group: Optional[AzureNetworkSecurityGroup] = None

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}' \
               f'/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Network/virtualNetworks/{self.network_name}/{self.name}'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def to_drift_detection_object(self) -> dict:
        return {'cidr_addresses': [str(cidr) for cidr in self.cidr_addresses],
                'network_security_group': self.network_security_group and self.network_security_group.to_drift_detection_object()
                }
