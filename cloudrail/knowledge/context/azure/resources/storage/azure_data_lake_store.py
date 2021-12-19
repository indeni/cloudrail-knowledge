from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.field_active import FieldActive


class DataLakeStoreTier(Enum):
    NONE = None
    CONSUMPTION = 'Consumption'
    COMMITMENT_1TB = 'Commitment_1TB'
    COMMITMENT_10TB = 'Commitment_10TB'
    COMMITMENT_100TB = 'Commitment_100TB'
    COMMITMENT_500TB = 'Commitment_500TB'
    COMMITMENT_1PB = 'Commitment_1PB'
    COMMITMENT_5PB = 'Commitment_5PB'


class AzureDataLakeStore(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Data Lake Analytics Store.
            tier: The monthly commitment tier.
            encryption_state: Enabling or disable encryption (allowed values: 'Enabled' or 'Disabled').
            encryption_type: Type of encryption used (allowed values: 'ServiceManaged' or '').
            identity: The type of identity which should be used for this Data Lake Store.
            firewall_allow_azure_ips: whether to allow or not Azure Service IPs through the firewall.
            firewall_state: The state of the firewall (allowed values: 'Enabled' or 'Disabled')
    """

    def __init__(self,
                 name: str,
                 tier: DataLakeStoreTier,
                 encryption_state: FieldActive,
                 encryption_type: str,
                 identity: Optional[str],
                 firewall_allow_azure_ips: FieldActive,
                 firewall_state: FieldActive):
        super().__init__(AzureResourceType.AZURERM_DATA_LAKE_STORE)
        self.name: str = name
        self.tier: DataLakeStoreTier = tier
        self.encryption_state: FieldActive = encryption_state
        self.encryption_type: str = encryption_type
        self.identity: Optional[str] = identity
        self.firewall_allow_azure_ips: FieldActive = firewall_allow_azure_ips
        self.firewall_state: FieldActive = firewall_state
        # Resources part of the context
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []
        self.with_aliases(self.name)

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.DataLakeStore/accounts/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Data Lake Store' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {
            'encryption_state': self.encryption_state,
            'encryption_type': self.encryption_type,
            'identity': self.identity,
            'firewall_allow_azure_ips': self.firewall_allow_azure_ips,
            'firewall_state': self.firewall_state,
        }

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings
