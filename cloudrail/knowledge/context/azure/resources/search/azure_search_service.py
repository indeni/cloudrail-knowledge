from typing import Optional, List
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import \
    AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings


class SearchServiceSku(str, Enum):
    BASIC = 'basic'
    FREE = 'free'
    STANDARD = 'standard'
    STANDARD2 = 'standard2'
    STANDARD3 = 'standard3'
    STORAGE_OPTIMIZED_L1 = 'storage_optimized_l1'
    STORAGE_OPTIMIZED_L2 = 'storage_optimized_l2'


class SearchServiceIdentityType(str, Enum):
    NONE = 'None'
    SYSTEM_ASSIGNED = 'SystemAssigned'
    USER_ASSIGNED = 'UserAssigned'
    USER_AND_SYSTEM_ASSIGNED = 'SystemAssigned, UserAssigned'


@dataclass
class SearchServiceIdentity:
    """
        Attributes:
            type: The Type of Identity which should be used for the Search Service.
    """
    type: SearchServiceIdentityType


class AzureSearchService(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The Name which should be used for this Search Service.
            sku: The SKU which should be used for this Search Service.
            public_network_access_enabled: Whether or not public network access is allowed for this resource.
            partition_count: The number of partitions which should be created.
            replica_count: The number of replica's which should be created.
            allowed_ips: A list of IPv4 addresses or CIDRs that are allowed access to the search service endpoint.
            identity: The Identity which should be used for the Search Service.
    """

    def __init__(self,
                 name: str,
                 sku: SearchServiceSku,
                 public_network_access_enabled: bool,
                 partition_count: int,
                 replica_count: int,
                 allowed_ips: Optional[List[str]],
                 identity: Optional[SearchServiceIdentity]):
        super().__init__(AzureResourceType.AZURERM_SEARCH_SERVICE)
        self.name: str = name
        self.sku: SearchServiceSku = sku
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.partition_count: int = partition_count
        self.replica_count: int = replica_count
        self.allowed_ips: Optional[List[str]] = allowed_ips
        self.identity: Optional[SearchServiceIdentity] = identity
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Search Service' + ('s' if is_plural else '')

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings

    def to_drift_detection_object(self) -> dict:
        return {'public_network_access_enabled': self.public_network_access_enabled,
                'partition_count': self.partition_count,
                'replica_count': self.replica_count,
                'allowed_ips': self.allowed_ips,
                'identity': self.identity,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]}
