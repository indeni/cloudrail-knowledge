from typing import Optional, List
from dataclasses import dataclass
from enum import Enum
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings


class BatchAccountPoolAllocationMode(Enum):
    BATCH_SERVICE = 'BatchService'
    USER_SUBSCRIPTION = 'UserSubscription'


@dataclass
class BatchAccountKeyVaultReference:
    """
        Attributes:
            name: The name of the Batch account to which this config belongs.
            id: The ID of the Azure KeyVault
            url: The HTTPS URL of the Azure KeyVault
    """
    name: str
    id: str
    url: str


class AzureBatchAccount(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The Batch account name
            monitor_diagnostic_settings: The monitoring settings of this Batch Account.
            pool_allocation_mode: Specifies the mode to use for pool allocation, BatchService (default) or UserSubscription.
            public_network_access_enabled: Whether public access is allowed for this server.  Defaults to true.
            key_vault_reference: A reference to KeyVault to use when deploying Batch account using UserSubscription pool allocation mode.
            storage_account_id: Specifies the storage account to use for the Batch account.
    """

    def __init__(self, name: str,
                 pool_allocation_mode: BatchAccountPoolAllocationMode,
                 public_network_access_enabled: bool,
                 key_vault_reference: Optional[BatchAccountKeyVaultReference],
                 storage_account_id: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_BATCH_ACCOUNT)
        self.name: str = name
        self.pool_allocation_mode: BatchAccountPoolAllocationMode = pool_allocation_mode
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.key_vault_reference: Optional[BatchAccountKeyVaultReference] = key_vault_reference
        self.storage_account_id: Optional[str] = storage_account_id
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'Batch Account' + ('s' if is_plural else '')

    def get_name(self) -> str:
        return self.name

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings

    def to_drift_detection_object(self) -> dict:
        return {'pool_allocation_mode': self.pool_allocation_mode,
                'public_network_access_enabled': self.public_network_access_enabled,
                'key_vault_reference': self.key_vault_reference,
                'storage_account_id': self.storage_account_id,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]}
