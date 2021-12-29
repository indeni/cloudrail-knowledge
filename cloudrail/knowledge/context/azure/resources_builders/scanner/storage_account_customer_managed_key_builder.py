from typing import Optional

from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_customer_managed_key import AzureStorageAccountCustomerManagedKey
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class StorageAccountCustomerManagedKeyBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'storage-accounts-list.json'

    def do_build(self, attributes: dict) -> Optional[AzureStorageAccountCustomerManagedKey]:
        properties = attributes["properties"]
        if key_vault_properties := properties["encryption"].get("keyvaultproperties"):
            storage_account_id = attributes["id"]
            key_vault_uri = key_vault_properties.get("keyvaulturi")
            key_vault_id = None
            key_name = key_vault_properties["keyname"]

            return AzureStorageAccountCustomerManagedKey(storage_account_id=storage_account_id,
                                                         key_vault_uri=key_vault_uri,
                                                         key_vault_id=key_vault_id,
                                                         key_name=key_name)
        return None
