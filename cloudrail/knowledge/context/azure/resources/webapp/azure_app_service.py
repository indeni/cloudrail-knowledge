from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_identity import Identity
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig


class AzureAppService(AzureResource):
    """
        Attributes:
            name: The name of this AppService.
            app_service_config: App service configuration.
            https_only: Indicates if the App Service only be accessed via HTTPS.
            client_cert_required: Indicate if client certificates are required in Web App.
    """
    def __init__(self, name: str, https_only: bool, client_cert_required: bool, identity: Optional[Identity]):
        super().__init__(AzureResourceType.AZURERM_APP_SERVICE)
        self.name: str = name
        self.app_service_config: AzureAppServiceConfig = None
        self.https_only: bool = https_only
        self.client_cert_required: bool = client_cert_required
        self.identity: Optional[Identity] = identity

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Web/sites/{self.name}/appServices'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'https_only': self.https_only,
                'client_cert_required': self.client_cert_required,
                'app_service_config': self.app_service_config and self.app_service_config.to_drift_detection_object()}
