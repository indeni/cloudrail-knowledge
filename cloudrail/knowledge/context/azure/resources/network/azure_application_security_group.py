from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureApplicationSecurityGroup(AzureResource):
    """
        Attributes:
            name: The application security group name.
    """

    def __init__(self,
                 name: str):
        super().__init__(AzureResourceType.AZURERM_APPLICATION_SECURITY_GROUP)
        self.name: str = name

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Network/applicationSecurityGroups/{self.name}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name}
