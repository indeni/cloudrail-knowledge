from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class IMonitorSettings:

    @abstractmethod
    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        pass
