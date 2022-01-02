from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity, ManagedIdentityType


class AzureAssignedUserIdentity(AzureManagedIdentity, AzureResource):

    """
        Attributes:
            identity_name: The assigned user identity name.
            client_id: Client id associated with the user assigned identity.
    """
    def __init__(self, identity_name: str = None, client_id: str = None, principal_id: str = None, tenant_id: str = None):
        AzureManagedIdentity.__init__(self, principal_id=principal_id, tenant_id=tenant_id,
                                      identity_type=ManagedIdentityType.USER_ASSIGNED)
        AzureResource.__init__(self, AzureResourceType.AZURERM_USER_ASSIGNED_IDENTITY)
        self.identity_name: str = identity_name
        self.client_id: str = client_id
        self.with_aliases(self.identity_name)

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> Optional[str]:
        return self.identity_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{self.identity_name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags}
