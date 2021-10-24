from typing import List, Optional
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules


class AzureStorageAccount(AzureResource):
    """
        Attributes:
            storage_name: The name of the storage account.
            account_tier: The Tier of the storage account.
            account_replication_type: The replication type of the storage account
            network_rules: The networking rules to allow or deny access from.
            enable_https_traffic_only: A flag indicating if only https traffic is allowed
            allow_blob_public_access: A flag indicator, True if enable public access to containers and blobs else disable.
    """
    def __init__(self, storage_name: str, account_tier: str, account_replication_type: str,
                 enable_https_traffic_only: bool, allow_blob_public_access: bool):
        super().__init__(AzureResourceType.AZURERM_STORAGE_ACCOUNT)
        self.storage_name: str = storage_name
        self.with_aliases(storage_name)
        self.account_tier: str = account_tier
        self.account_replication_type: str = account_replication_type
        self.enable_https_traffic_only: bool = enable_https_traffic_only
        self.network_rules: AzureStorageAccountNetworkRules = None
        self.allow_blob_public_access: bool = allow_blob_public_access

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.storage_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        return 'Storage ' + 'Account' if not is_plural else 'Accounts'

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'storage_name': self.storage_name,
                'account_tier': self.account_tier,
                'account_replication_type': self.account_replication_type,
                'enable_https_traffic_only': self.enable_https_traffic_only,
                'allow_blob_public_access': self.allow_blob_public_access,
                'network_rules': self.network_rules and self.network_rules.to_drift_detection_object()}
