from cloudrail.knowledge.context.azure.resources.search.azure_search_service import AzureSearchService, SearchServiceSku, \
    SearchServiceIdentity, SearchServiceIdentityType
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation
from cloudrail.knowledge.utils.utils import is_iterable_with_values

class SearchServiceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-search-services.json'

    def do_build(self, attributes: dict) -> AzureSearchService:
        properties = attributes['properties']

        ## Allowed IP's
        allowed_ips = properties['networkRuleSet']['ipRules']
        if is_iterable_with_values(allowed_ips):
            allowed_ips = [ip['value'] for ip in properties['networkRuleSet']['ipRules']]

        ## Identity
        identity = None
        if identity_data := attributes.get('identity'):
            identity = SearchServiceIdentity(enum_implementation(SearchServiceIdentityType, identity_data['type']))
        return AzureSearchService(name=attributes['name'],
                                  sku=enum_implementation(SearchServiceSku, attributes['sku']['name']),
                                  public_network_access_enabled=properties['publicNetworkAccess'] == 'enabled',
                                  partition_count=properties['partitionCount'],
                                  replica_count=properties['replicaCount'],
                                  allowed_ips=allowed_ips,
                                  identity=identity)
