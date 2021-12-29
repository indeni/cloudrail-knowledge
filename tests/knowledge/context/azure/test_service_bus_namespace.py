from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.service_bus.azure_service_bus_namespace import ServiceBusNamespaceSku
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestServiceBusNamespace(AzureContextTest):

    def get_component(self):
        return "service_bus_namespace"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        sb_namespace = next((service_bus for service_bus in ctx.service_bus_namespaces if service_bus.name == 'cr3688-servicebus-namespace'), None)
        self.assertIsNotNone(sb_namespace)
        self.assertEqual(sb_namespace.capacity, 0)
        self.assertFalse(sb_namespace.zone_redundant)
        self.assertEqual(sb_namespace.sku, ServiceBusNamespaceSku.BASIC)
