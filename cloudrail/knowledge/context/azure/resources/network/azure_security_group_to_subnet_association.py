from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureSecurityGroupToSubnetAssociation(AzureResource):
    """
        Attributes:
            subnet_id: The subnet id which needs to be connected to the network security group.
            network_security_group_id: The network security group id which needs to be connected to the subnet.
    """
    def __init__(self, subnet_id: str, network_security_group_id: str):
        super().__init__(AzureResourceType.AZURERM_SUBNET_NETWORK_SECURITY_GROUP_ASSOCIATION)
        self.subnet_id: str = subnet_id
        self.network_security_group_id = network_security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subnet_id, self.network_security_group_id]

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'subnet_id': self.subnet_id,
                'network_security_group_id': self.network_security_group_id}
