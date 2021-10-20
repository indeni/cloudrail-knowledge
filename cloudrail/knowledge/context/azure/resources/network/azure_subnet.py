from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup


class AzureSubnet(AzureResource):
    """
        Attributes:
            name: The name of this subnet
            network_security_group: The actual security group that's attached to this subnet.
    """

    def __init__(self, name: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name

        self.network_security_group: Optional[AzureNetworkSecurityGroup] = None

    def get_cloud_resource_url(self) -> Optional[str]:
        pass  # Requires VNET

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name}
