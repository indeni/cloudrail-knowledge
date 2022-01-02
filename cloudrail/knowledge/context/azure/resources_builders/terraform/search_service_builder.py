from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.search.azure_search_service import AzureSearchService, SearchServiceSku, \
    SearchServiceIdentity, SearchServiceIdentityType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class SearchServiceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSearchService:
        identity = None
        if identity_data := self._get_known_value(attributes, 'identity'):
            identity = SearchServiceIdentity(type=SearchServiceIdentityType(self._get_known_value(identity_data[0], 'type','SystemAssigned')))
        return AzureSearchService(name=attributes['name'],
                                  sku=enum_implementation(SearchServiceSku, attributes['sku']),
                                  public_network_access_enabled=self._get_known_value(attributes, 'public_network_access_enabled', True),
                                  partition_count=self._get_known_value(attributes, 'partition_count', 1),
                                  replica_count=self._get_known_value(attributes, 'replica_count', 1),
                                  allowed_ips=self._get_known_value(attributes, 'allowed_ips', []),
                                  identity=identity)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SEARCH_SERVICE
