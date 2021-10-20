from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureNetworkInterfaceApplicationSecurityGroupAssociation(AzureResource):
    """
        Attributes:
            network_interface_id: The network interface id which needs to be connected to the application security group.
            application_security_group_id: The application security group id which needs to be connected to the network interface.
    """

    def __init__(self, network_interface_id: str, application_security_group_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE_APPLICATION_SECURITY_GROUP_ASSOCIATION)
        self.network_interface_id: str = network_interface_id
        self.application_security_group_id = application_security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'network_interface_id': self.network_interface_id,
                'application_security_group_id': self.application_security_group_id}
