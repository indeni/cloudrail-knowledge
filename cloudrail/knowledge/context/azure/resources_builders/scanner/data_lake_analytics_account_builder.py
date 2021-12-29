from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_analytics_account import AzureDataLakeAnalyticsAccount, DataLakeAnalyticsAccountTier
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder

class DataLakeAnalyticsAccountBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return  'datalakeanalytics-account-data.json'

    def do_build(self, attributes: dict) -> AzureDataLakeAnalyticsAccount:
        account_propertries = attributes['properties']
        return AzureDataLakeAnalyticsAccount(name=attributes['name'],
                                             default_store_account_name=account_propertries['defaultDataLakeStoreAccount'],
                                             tier=DataLakeAnalyticsAccountTier(account_propertries['currentTier']))
