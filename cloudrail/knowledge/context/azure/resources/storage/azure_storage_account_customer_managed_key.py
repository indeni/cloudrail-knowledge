from typing import List, Optional
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureStorageAccountCustomerManagedKey(AzureResource):
    """
        Attributes:
            storage_account_id: The ID of the Storage Account. Changing this forces a new resource to be created.
            key_vault_uri: The URI of the Key Vault.
            key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
            key_name: The name of Key Vault Key.
    """

    def __init__(self, storage_account_id: str, key_vault_uri: Optional[str], key_vault_id: str, key_name: str):
        super().__init__(AzureResourceType.AZURERM_STORAGE_ACCOUNT_CUSTOMER_MANAGED_KEY)
        self.storage_account_id: str = storage_account_id
        self.key_vault_uri: Optional[str] = key_vault_uri
        self.key_vault_id: str = key_vault_id
        self.key_name: str = key_name

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return f"Storage account customer managed key of {self.get_id()}"

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False

    def get_type(self, is_plural: bool = False) -> str:
        return 'Storage Account Customer Managed ' + 'Key' if not is_plural else 'keys'

    def to_drift_detection_object(self) -> dict:
        return {"key_vault_id": self.key_vault_id,
                "key_name": self.key_name}
