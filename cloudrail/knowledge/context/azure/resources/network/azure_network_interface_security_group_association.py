from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureNetworkInterfaceSecurityGroupAssociation(AzureResource):
    """
        Attributes:
            network_interface_id: The network interface id which needs to be connected to the network security group.
            network_security_group_id: The network security group id which needs to be connected to the network interface.
    """

    def __init__(self, network_interface_id: str, network_security_group_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE_SECURITY_GROUP_ASSOCIATION)
        self.network_interface_id: str = network_interface_id
        self.network_security_group_id = network_security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.network_interface_id, self.network_security_group_id]

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'network_interface_id': self.network_interface_id,
                'network_security_group_id': self.network_security_group_id}
