from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.webapp.constants import FtpsState
from cloudrail.knowledge.context.azure.webapp.diagnostic_logs import DiagnosticLogs


class AzureAppServiceConfig(AzureResource):
    """
        Attributes:
            name: The name of the AppService to which this config belongs.
            ftps_state: The FTPS state defined in this config. Either AllAllowed, FTPSOnly or Disabled.
            auth_settings: App service authentication settings.
            minimum_tls_version: The minimum supported TLS version for the function app.
            http2_enabled: Indication if http2 protocol should be enabled or not.
            logs: The DiagnosticLogs indicate if the logs (detailed error messages, HTTP logging, and failed requests tracing) are enabled or not

    """

    def __init__(self, name, ftps_state: FtpsState, auth_settings: AuthSettings, minimum_tls_version: str, http2_enabled: bool, logs: DiagnosticLogs):
        super().__init__(AzureResourceType.NONE)
        self.name: str = name
        self.ftps_state: FtpsState = ftps_state
        self.auth_settings: AuthSettings = auth_settings
        self.minimum_tls_version: str = minimum_tls_version
        self.http2_enabled: bool = http2_enabled
        self.logs: DiagnosticLogs = logs


    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Web/sites/{self.name}/configuration'

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False
