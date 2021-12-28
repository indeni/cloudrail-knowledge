from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.i_managed_identity_resource import IManagedIdentityResource
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode


class AzureFunctionApp(AzureResource, IManagedIdentityResource):
    """
        Attributes:
            name: Function app resource name.
            app_service_config: App service configuration.
            client_cert_mode: The mode of the Function App's client certificates requirement for incoming requests.
            https_only: Indicates if the Function App only be accessed via HTTPS.
            identities_ids: The managed identities associated with the function app.
            managed_identities: all managed identities associate with the function app.
    """

    def __init__(self, name: str,
                 client_cert_mode: FieldMode,
                 https_only: bool,
                 identities_ids: List[str]):
        super().__init__(AzureResourceType.AZURERM_FUNCTION_APP)
        self.name = name
        self.app_service_config: AzureAppServiceConfig = None
        self.client_cert_mode: FieldMode = client_cert_mode
        self.https_only = https_only
        self.with_aliases(name)
        self.identities_ids: List[str] = identities_ids
        self.managed_identities: List[AzureManagedIdentity] = []

    def get_keys(self) -> List[str]:
        return [self.get_id()]

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

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'client_cert_mode': self.client_cert_mode.value,
                'https_only': self.https_only,
                'app_service_config': self.app_service_config.to_drift_detection_object()}

    def get_managed_identities(self) -> List[AzureManagedIdentity]:
        return self.managed_identities

    def get_managed_identities_ids(self) -> List[str]:
        return self.identities_ids
