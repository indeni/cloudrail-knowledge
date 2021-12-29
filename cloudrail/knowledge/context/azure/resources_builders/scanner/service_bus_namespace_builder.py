from cloudrail.knowledge.context.azure.resources.service_bus.azure_service_bus_namespace import AzureServiceBusNamespace, ServiceBusNamespaceSku
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class ServiceBusNamespaceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-servicebus-namespaces.json'

    def do_build(self, attributes: dict) -> AzureServiceBusNamespace:
        properties = attributes['properties']
        sku_attributes = attributes['sku']
        return AzureServiceBusNamespace(name=attributes['name'],
                                        sku=ServiceBusNamespaceSku(sku_attributes['name']),
                                        capacity=sku_attributes.get('capacity', 0),
                                        zone_redundant=properties.get('zoneRedundant', False))
