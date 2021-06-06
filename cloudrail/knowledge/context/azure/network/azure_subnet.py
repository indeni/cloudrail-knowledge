from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup


class AzureSubnet(AzureResource):
    """
        Attributes:
            name: The name of this subnet
            security_group_id: The id of the security group thats attached to this subnet
            security_group: The actual security group thats attached to this subnet
    """

    def __init__(self, security_group_id: Optional[str], name: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.security_group_id: str = security_group_id
        self.name: str = name

        self.security_group: AzureNetworkSecurityGroup = None

    def get_cloud_resource_url(self) -> Optional[str]:
        pass  # Requires VNET

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]
