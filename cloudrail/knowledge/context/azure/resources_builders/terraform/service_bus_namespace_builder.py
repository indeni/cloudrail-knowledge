from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.service_bus.azure_service_bus_namespace import AzureServiceBusNamespace, ServiceBusNamespaceSku
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class ServiceBusNamespaceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureServiceBusNamespace:
        return AzureServiceBusNamespace(name=attributes['name'],
                                        sku=enum_implementation(ServiceBusNamespaceSku, attributes['sku']),
                                        capacity=self._get_known_value(attributes, 'capacity', 0),
                                        zone_redundant=self._get_known_value(attributes, 'zone_redundant', False))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SERVICEBUS_NAMESPACE
