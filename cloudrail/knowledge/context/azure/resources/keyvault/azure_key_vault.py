from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class AzureKeyVault(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The KeyVault name
            monitor_diagnostic_settings: The monitoring settings of this KeyVault
            purge_protection_enabled: Indication if Purge Protection is enabled for this KeyVault
    """

    def __init__(self, name: str, purge_protection_enabled: bool):
        super().__init__(AzureResourceType.AZURERM_KEY_VAULT)
        self.name: str = name
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []
        self.purge_protection_enabled: bool = purge_protection_enabled

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.KeyVault/vaults/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'Key ' + 'Vault' if not is_plural else 'Vaults'

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'purge_protection_enabled': self.purge_protection_enabled,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]
                }

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings
