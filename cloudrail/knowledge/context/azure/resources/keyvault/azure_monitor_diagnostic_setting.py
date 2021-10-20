from dataclasses import dataclass
from typing import Optional, List

import dataclasses
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


@dataclass
class AzureMonitorDiagnosticLogsRetentionPolicySettings:
    enabled: bool
    days: int


@dataclass
class AzureMonitorDiagnosticLogsSettings:
    enabled: bool
    retention_policy: Optional[AzureMonitorDiagnosticLogsRetentionPolicySettings]


class AzureMonitorDiagnosticSetting(AzureResource):
    """
        Attributes:
            name: The monitor diagnostic setting's name
            target_resource_id: The ID of the resource that is monitored
            logs_settings: The logs settings
    """
    def __init__(self, name: str, target_resource_id: str, logs_settings: Optional[AzureMonitorDiagnosticLogsSettings]):
        super().__init__(AzureResourceType.AZURERM_MONITOR_DIAGNOSTIC_SETTING)
        self.name: str = name
        self.target_resource_id: str = target_resource_id
        self.logs_settings: Optional[AzureMonitorDiagnosticLogsSettings] = logs_settings
        self.with_aliases(target_resource_id)

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/{self.target_resource_id}/diagnostics'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self._id]

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'target_resource_id': self.target_resource_id,
                'logs_settings': self.logs_settings and dataclasses.asdict(self.logs_settings)}
