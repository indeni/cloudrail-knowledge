from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureSecurityCenterAutoProvisioning(AzureResource):
    """
        Attributes:
            auto_provision_is_on: A flag indicating if auto provision is on
    """

    def __init__(self, auto_provision_is_on: bool):
        super().__init__(AzureResourceType.AZURERM_SECURITY_CENTER_AUTO_PROVISIONING)
        self.auto_provision_is_on: bool = auto_provision_is_on

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#blade/Microsoft_Azure_Security/PolicyMenuBlade/dataCollection/subscriptionId/' \
               f'{self.subscription_id}/pricingTier/0'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subscription_id]

    def to_drift_detection_object(self) -> dict:
        return {'auto_provision_is_on': self.auto_provision_is_on}
