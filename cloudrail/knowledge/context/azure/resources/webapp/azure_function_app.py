from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode


class AzureFunctionApp(AzureResource):
    """
        Attributes:
            name: Function app resource name.
            app_service_config: App service configuration.
            client_cert_mode: The mode of the Function App's client certificates requirement for incoming requests.
            https_only: Indicates if the Function App only be accessed via HTTPS
    """
    def __init__(self, name: str,
                 client_cert_mode: FieldMode,
                 https_only: bool):
        super().__init__(AzureResourceType.AZURERM_FUNCTION_APP)
        self.name = name
        self.app_service_config: AzureAppServiceConfig = None
        self.client_cert_mode: FieldMode = client_cert_mode
        self.https_only = https_only
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.name, self.location]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Function App'
        else:
            return 'Function Apps'

    @property
    def is_tagable(self) -> bool:
        return True
