from typing import Optional, List
from enum import Enum

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class ServiceBusNamespaceSku(Enum):
    BASIC = 'Basic'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'


class AzureServiceBusNamespace(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Service Bus Namespace.
            sku: The SKU of the Service Bus Namespace.
            capacity: The capacity of the Service Bus Namespace.
            zone_reduntant: Whether or not this resource is zone redundant.
    """

    def __init__(self,
                 name: str,
                 sku: ServiceBusNamespaceSku,
                 capacity: int,
                 zone_redundant: bool):
        super().__init__(AzureResourceType.AZURERM_SERVICEBUS_NAMESPACE)
        self.name: str = name
        self.sku: ServiceBusNamespaceSku = sku
        self.capacity: int = capacity
        self.zone_redundant: bool = zone_redundant
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
        return 'Service Bus Namespace' + ('s' if is_plural else '')

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags,
                'capacity': self.capacity,
                'zone_redundant': self.zone_redundant,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]}
