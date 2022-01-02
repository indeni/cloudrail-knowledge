from typing import List

from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import _get_known_value
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_terraform_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class EventHubNamespaceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        identity = create_terraform_system_managed_identity(attributes)
        managed_identities: List[AzureManagedIdentity] = []
        if identity:
            managed_identities.append(identity)
        return AzureEventHubNamespace(name=attributes['name'],
                                      sku=EventHubNamespaceSku(attributes['sku']),
                                      capacity=attributes.get('capacity', 2),
                                      auto_inflate_enabled=attributes.get('auto_inflate_enabled', False),
                                      managed_identities=managed_identities,
                                      maximum_throughput_units=int(_get_known_value(attributes, 'maximum_throughput_units', 0)))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_EVENTHUB_NAMESPACE
