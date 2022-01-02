from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet
from cloudrail.knowledge.context.azure.resources.i_managed_identity_resource import IManagedIdentityResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class EventHubNamespaceSku(Enum):
    BASIC = 'Basic'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'


class AzureEventHubNamespace(AzureResource, IMonitorSettings, IManagedIdentityResource):
    """
        Attributes:
            name: The name of the Data Lake Analytics Store.
            sku: Defines which tier to use (allowed values: Basic, Standard, and Premium).
            capacity: Specifies the capacity units for a Standard SKU namespace.
            auto_inflate_enabled: Enable or disable Auto Inflate for the EventHub Namespace.
            managed_identities: all managed identities associate with the EventHub Namespace.
            maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is enabled.
            network_rule_set: Set of network rules to control access to the EventHub Namespace.
    """

    def __init__(self,
                 name: str,
                 sku: EventHubNamespaceSku,
                 capacity: int,
                 auto_inflate_enabled: bool,
                 managed_identities: List[AzureManagedIdentity],
                 maximum_throughput_units: int):
        super().__init__(AzureResourceType.AZURERM_EVENTHUB_NAMESPACE)
        self.name: str = name
        self.sku: EventHubNamespaceSku = sku
        self.capacity: int = capacity
        self.auto_inflate_enabled: bool = auto_inflate_enabled
        self.managed_identities: List[AzureManagedIdentity] = managed_identities
        self.maximum_throughput_units: int = maximum_throughput_units
        self.network_rule_set: Optional[EventHubNetworkRuleSet] = None
        self._monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.EventHub/namespaces/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'EventHub Namespace' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {'sku': self.sku.value,
                'capacity': self.capacity,
                'auto_inflate_enabled': self.auto_inflate_enabled,
                'managed_identities': [identity.to_drift_detection_object() for identity in self.managed_identities],
                'maximum_throughput_units': self.maximum_throughput_units,
                'network_rule_set': self.network_rule_set and self.network_rule_set.to_drift_detection_object(),
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self._monitor_diagnostic_settings]
                }

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self._monitor_diagnostic_settings

    def get_managed_identities(self) -> List[AzureManagedIdentity]:
        return self.managed_identities

    def get_managed_identities_ids(self) -> List[str]:
        return []
