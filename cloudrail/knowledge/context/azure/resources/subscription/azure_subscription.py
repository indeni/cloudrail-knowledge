from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert


class AzureSubscription(AzureResource):
    """
        Attributes:
            subscription_name: The Name of the Subscription.
            subscription_id: The ID of the Subscription.
    """

    def __init__(self,
                 subscription_name: str,
                 subscription_id: str):
        super().__init__(AzureResourceType.AZURERM_SUBSCRIPTION)
        self.subscription_name: str = subscription_name
        self.subscription_id: str = subscription_id
        self.monitor_activity_alert_log_list: List[AzureMonitorActivityLogAlert] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.subscription_name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Subscription' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {"tags": self.tags}
