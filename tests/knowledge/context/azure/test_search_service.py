from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.search.azure_search_service import SearchServiceSku, SearchServiceIdentity, \
    SearchServiceIdentityType
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSearchService(AzureContextTest):

    def get_component(self):
        return "search_service"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        search_service = next((service for service in ctx.search_services if service.name == 'cr3687-search-service'), None)
        self.assertIsNotNone(search_service)
        self.assertFalse(search_service.public_network_access_enabled)
        self.assertEqual(search_service.sku, SearchServiceSku.STANDARD)
        self.assertEqual(search_service.partition_count, 1)
        self.assertEqual(search_service.replica_count, 1)
        self.assertEqual(search_service.allowed_ips, ["8.8.8.8"])
        self.assertEqual(search_service.identity, SearchServiceIdentity(SearchServiceIdentityType.SYSTEM_ASSIGNED))
