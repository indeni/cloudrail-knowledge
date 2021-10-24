from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class VirtualNetworkGatewayType(Enum):
    VPN = 'Vpn'
    EXPRESS_ROUTE = 'ExpressRoute'
    LOCAL_GATEWAY = 'LocalGateway'


class AzureVirtualNetworkGateway(AzureResource):
    """
        Attributes:
            name: The GW name
            gateway_type: The GW type
            sku_tier: The GW SKU tier (Basic, Standard, etc)
    """

    def __init__(self, name: str, gateway_type: VirtualNetworkGatewayType, sku_tier: str) -> None:
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_NETWORK_GATEWAY)
        self.name: str = name
        self.gateway_type: VirtualNetworkGatewayType = gateway_type
        self.sku_tier: str = sku_tier

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/virtualNetworkGateways/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'gateway_type': self.gateway_type.value,
                'sku_tier': self.sku_tier}
