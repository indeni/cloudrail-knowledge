from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzurePublicIp(AzureResource):
    """
        Attributes:
            name: The name of this Public IP
            public_ip_address: The actual public ip address.
    """
    def __init__(self, name: str, public_ip_address: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_PUBLIC_IP)
        self.name = name
        self.public_ip_address = public_ip_address

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Network/publicIPAddresses/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'public_ip_address': self.public_ip_address}
