from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.load_balancer.load_balancer_frontend_ip_configuration import LoadBalancerFrontendIpConfiguration
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_probe import AzureLoadBalancerProbe
from cloudrail.knowledge.utils.tags_utils import filter_tags


class AzureLoadBalancerSku(Enum):
    BASIC = 'Basic'
    STANDARD = 'Standard'
    GATEWAY = 'Gateway'


class AzureLoadBalancerSkuTier(Enum):
    GLOBAL = 'Global'
    REGIONAL = 'Regional'


class AzureLoadBalancer(AzureResource):
    """
        Attributes:
            name: The name of the Load Balancer.
            sku: The Sku of the Load Balancer.
            sku_tier: The Sku Tier of the Load Balancer.
            frontend_ip_configurations: A List of frontend IP configurations.
    """
    def __init__(self,
                 name: str,
                 sku: AzureLoadBalancerSku,
                 sku_tier: AzureLoadBalancerSkuTier,
                 frontend_ip_configurations: List[LoadBalancerFrontendIpConfiguration]):
        super().__init__(AzureResourceType.AZURERM_LB)
        self.name: str = name
        self.sku: AzureLoadBalancerSku = sku
        self.sku_tier: AzureLoadBalancerSkuTier = sku_tier
        self.frontend_ip_configurations: List[LoadBalancerFrontendIpConfiguration] = frontend_ip_configurations
        self.probes: Optional[List[AzureLoadBalancerProbe]] = []
        # self.inbound_nat_rules: Optional[List[AzureLoadBalancerNatRule]] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Load Balancer' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {
            'tags': filter_tags(self.tags),
            'sku': self.sku and self.sku.value,
            'sku_tier': self.sku_tier and self.sku_tier.value,
            'frontend_ip_configurations': [conf.to_drift_detection_object() for conf in self.frontend_ip_configurations]
        }
