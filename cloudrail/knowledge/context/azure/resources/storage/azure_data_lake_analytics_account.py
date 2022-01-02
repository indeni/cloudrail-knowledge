from typing import Optional, List
from enum import Enum
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class DataLakeAnalyticsAccountTier(str, Enum):
    CONSUMPTION = 'Consumption'
    COMMITMENT100000AUHOURS = 'Commitment_100000AUHours'
    COMMITMENT10000AUHOURS = 'Commitment_10000AUHours'
    COMMITMENT1000AUHOURS = 'Commitment_1000AUHours'
    COMMITMENT100AUHOURS = 'Commitment_100AUHours'
    COMMITMENT500000AUHOURS = 'Commitment_500000AUHours'
    COMMITMENT50000AUHOURS = 'Commitment_50000AUHours'
    COMMITMENT5000AUHOURS = 'Commitment_5000AUHours'
    COMMITMENT500AUHOURS = 'Commitment_500AUHours'


class AzureDataLakeAnalyticsAccount(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Data Lake Analytics Account.
            default_store_account_name: The name of the Data Lake Storage to be used.
            tier: The monthly commitment tier.
    """

    def __init__(self,
                 name: str,
                 default_store_account_name: str,
                 tier: DataLakeAnalyticsAccountTier):
        super().__init__(AzureResourceType.AZURERM_DATA_LAKE_ANALYTICS_ACCOUNT)
        self.name: str = name
        self.tier: DataLakeAnalyticsAccountTier = tier
        self.default_store_account_name: str = default_store_account_name
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Data Lake Analytics Account' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {
            'tags': self.tags,
            'tier': self.tier,
            'default_store_account_name': self.default_store_account_name,
            'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]
        }

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings
