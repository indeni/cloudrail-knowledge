from typing import List

from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_scanner_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class EventHubNamespaceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-event-hub-namespaces.json'

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        properties: dict = attributes['properties']
        identity = create_scanner_system_managed_identity(attributes)
        managed_identities: List[AzureManagedIdentity] = []
        if identity:
            managed_identities.append(identity)
        return AzureEventHubNamespace(name=attributes['name'],
                                      sku=EventHubNamespaceSku(attributes['sku']['tier']),
                                      capacity=attributes['sku']['capacity'],
                                      auto_inflate_enabled=properties['isAutoInflateEnabled'],
                                      managed_identities=managed_identities,
                                      maximum_throughput_units=properties['maximumThroughputUnits'])
