from abc import abstractmethod
from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface


class NetworkResource(AzureResource):
    def __init__(self, resource_type: AzureResourceType):
        super().__init__(resource_type)
        self.network_interfaces: List[AzureNetworkInterface] = []

    @property
    def inbound_connections(self):
        return [inbound_connection for nic in self.network_interfaces for inbound_connection in nic.inbound_connections]

    @property
    def outbound_connections(self):
        return [outbound_connection for nic in self.network_interfaces for outbound_connection in nic.outbound_connections]

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass
