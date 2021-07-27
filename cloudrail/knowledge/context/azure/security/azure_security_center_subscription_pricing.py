from enum import Enum
from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class SubscriptionPricingTier(str, Enum):
    FREE = 'Free'
    STANDARD = 'Standard'


class SubscriptionPricingResourceType(str, Enum):
    APP_SERVICES = 'AppServices'
    CONTAINER_REGISTRY = 'ContainerRegistry'
    KEY_VAULTS = 'KeyVaults'
    KUBERNETES_SERVICE = 'KubernetesService'
    SQL_SERVERS = 'SqlServers'
    SQL_SERVER_VIRTUAL_MACHINES = 'SqlServerVirtualMachines'
    STORAGE_ACCOUNTS = 'StorageAccounts'
    VIRTUAL_MACHINES = 'VirtualMachines'
    ARM = 'Arm'
    DNS = 'Dns'
    OPEN_SOURCE_RELATIONAL_DATABASES = 'OpenSourceRelationalDatabases'


class AzureSecurityCenterSubscriptionPricing(AzureResource):
    """
        Attributes:
            tier: The pricing tier.
            resource_type: The resource type this tier applies to.
    """

    def __init__(self, tier: SubscriptionPricingTier, resource_type: SubscriptionPricingResourceType):
        super().__init__(AzureResourceType.AZURERM_SECURITY_CENTER_SUBSCRIPTION_PRICING)
        self.tier: SubscriptionPricingTier = tier
        self.resource_type: SubscriptionPricingResourceType = resource_type

    def get_cloud_resource_url(self) -> Optional[str]:
        return 'https://portal.azure.com/#blade/Microsoft_Azure_Security/SecurityMenuBlade/pricingTier'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.resource_type]
