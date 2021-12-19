from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_analytics_account import AzureDataLakeAnalyticsAccount, DataLakeAnalyticsAccountTier
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class DataLakeAnalyticsAccountBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureDataLakeAnalyticsAccount:
        return AzureDataLakeAnalyticsAccount(name=attributes['name'],
                                             default_store_account_name=attributes['default_store_account_name'],
                                             tier=DataLakeAnalyticsAccountTier(self._get_known_value(attributes, 'tier', 'Consumption')))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_DATA_LAKE_ANALYTICS_ACCOUNT
