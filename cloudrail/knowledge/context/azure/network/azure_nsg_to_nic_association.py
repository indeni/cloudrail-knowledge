from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureNetworkSecurityGroupToNicAssociation(AzureResource):
    """
        Attributes:
            nic_id: The network interface id which needs to be connected to the NSG.
            network_security_group_id: The network security group id which needs to be connected to the NIC.
    """

    def __init__(self, nic_id: str, network_security_group_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE_SECURITY_GROUP_ASSOCIATION)
        self.nic_id: str = nic_id
        self.network_security_group_id = network_security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.nic_id, self.network_security_group_id]
