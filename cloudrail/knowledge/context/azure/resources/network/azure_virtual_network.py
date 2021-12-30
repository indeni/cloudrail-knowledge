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
    """
    def __init__(self, network_name: str, cidr_addresses: List[ipaddress.IPv4Network]):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_NETWORK)
        self.network_name: str = network_name
        self.cidr_addresses: List[ipaddress.IPv4Network] = cidr_addresses
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
            'subnets': [subnet.to_drift_detection_object() for subnet in self.subnets.values()]
        }
