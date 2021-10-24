from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureKubernetesCluster(AzureResource):
    def __init__(self, name: str, enable_rbac: bool):
        super().__init__(AzureResourceType.AZURERM_KUBERNETES_CLUSTER)
        self.name: str = name
        self.enable_rbac: bool = enable_rbac

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.ContainerService/managedClusters/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'enable_rbac': self.enable_rbac}
