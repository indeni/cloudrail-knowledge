from abc import abstractmethod
from typing import List, Set
from dataclasses import dataclass
from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.utils.utils import flat_list
from cloudrail.knowledge.context.connection import ConnectionInstance, ConnectionDetail, ConnectionType
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.context.gcp.resources.networking_config.network_interface import GcpNetworkInterface
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, FirewallRuleAction

@dataclass
class GcpConnection(ConnectionDetail):
    connection_type: ConnectionType
    firewall_action: FirewallRuleAction
    priority: int
    firewall: GcpComputeFirewall

    def compare_conn(self, other) -> bool:
        return self.connection_property == other.connection_property \
            and self.connection_type == other.connection_type \
                and self.connection_direction_type == other.connection_direction_type


class NetworkEntity(GcpResource, ConnectionInstance):
    """
        This class is the parent of all resources that have a network connection.

        Attributes:
            network_interfaces: The network interfaces used by this network entity.
    """
    def __init__(self,
                 network_interfaces: List[GcpNetworkInterface]) -> None:
        super().__init__(GcpResourceType.NONE)
        ConnectionInstance.__init__(self)
        self.network_interfaces: List[GcpNetworkInterface] = network_interfaces
        self.forwarding_rules: List[GcpComputeForwardingRule] = []
        self.inbound_connections: List[GcpConnection] = []
        self.outbound_connections: List[GcpConnection] = []

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        pass

    @property
    def is_labeled(self) -> bool:
        pass

    @property
    def vpc_networks(self) -> Set[GcpComputeNetwork]:
        return {nic.vpc_network for nic in self.network_interfaces}

    @property
    def firewalls(self) -> Set[GcpComputeFirewall]:
        return {firewall for nic in self.network_interfaces for firewall in nic.firewalls}

    @property
    def forward_rule_port_range(self) -> List[PortSet]:
        return flat_list([rule.port_range for rule in self.forwarding_rules])

    @property
    def public_ip_addresses(self) -> List[str]:
        return flat_list([nic.public_ips for nic in self.network_interfaces])

    @property
    def private_ip_addresses(self) -> List[str]:
        return [nic.private_ip for nic in self.network_interfaces]
