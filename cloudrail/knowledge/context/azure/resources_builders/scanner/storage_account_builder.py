
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class StorageAccountBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'storage-accounts-list.json'

    def do_build(self, attributes: dict) -> AzureStorageAccount:
        return AzureStorageAccount(storage_name=attributes['name'],
                                   account_tier=attributes['sku']['tier'],
                                   account_replication_type=attributes['sku']['name'].split('_').pop(),
                                   enable_https_traffic_only=attributes['properties']['supportsHttpsTrafficOnly'],
                                   allow_blob_public_access=attributes['properties']['allowBlobPublicAccess'])
