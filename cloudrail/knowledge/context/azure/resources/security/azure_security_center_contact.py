from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureSecurityCenterContact(AzureResource):
    """
        Attributes:
            alert_notifications: A flag indicating if alert notifications is on
    """

    def __init__(self, alert_notifications: bool):
        super().__init__(AzureResourceType.AZURERM_SECURITY_CENTER_CONTACT)
        self.alert_notifications: bool = alert_notifications

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#blade/Microsoft_Azure_Security/PolicyMenuBlade/emailNotifications/subscriptionId/' \
               f'{self.subscription_id}/pricingTier/0/defaultId/'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subscription_id]

    def to_drift_detection_object(self) -> dict:
        return {'alert_notifications': self.alert_notifications}
