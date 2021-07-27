from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureStorageAccount(AzureResource):
    """
        Attributes:
            name: the name of the storage account
            enable_https_traffic_only: A flag indicating if only https traffic is allowed
    """

    def __init__(self, name: str, enable_https_traffic_only: bool):
        super().__init__(AzureResourceType.AZURERM_STORAGE_ACCOUNT)
        self.name = name
        self.enable_https_traffic_only = enable_https_traffic_only

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Storage/storageAccounts/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]
