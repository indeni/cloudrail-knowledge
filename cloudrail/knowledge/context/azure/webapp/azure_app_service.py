from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class FtpState(Enum):
    ALL_ALLOWED = 'AllAllowed'
    FTPS_ONLY = 'FtpsOnly'
    DISABLED = 'Disabled'


class SiteConfig:

    def __init__(self, ftp_state: FtpState) -> None:
        super().__init__()
        self.ftp_state: FtpState = ftp_state


class AzureAppService(AzureResource):

    def __init__(self, name: str, app_service_plan_id: str, site_config: SiteConfig = None) -> None:
        super().__init__(AzureResourceType.AZURERM_APP_SERVICE)
        self.name = name
        self.app_service_plan_id: str = app_service_plan_id
        self.site_config: SiteConfig = site_config
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False
