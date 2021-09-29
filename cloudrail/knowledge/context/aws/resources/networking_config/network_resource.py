from typing import List, Set, Optional

from cloudrail.knowledge.context.connection import ConnectionDetail
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.route import Route
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet


class NetworkResource:

    def __init__(self):
        self.network_interfaces: List[NetworkInterface] = []

    def add_interface(self, eni: NetworkInterface) -> None:
        if eni in self.network_interfaces:
            self.network_interfaces.remove(eni)
        self.network_interfaces.append(eni)

    @property
    def private_ip_addresses(self) -> List[str]:
        secondary_ip_addresses = [private_ip for network_interface in self.network_interfaces
                                  for private_ip in network_interface.secondary_ip_addresses]
        primary_ip_addresses = [network_interface.primary_ip_address for network_interface in self.network_interfaces]
        return secondary_ip_addresses + primary_ip_addresses

    @property
    def public_ip_addresses(self) -> List[str]:
        return [network_interface.public_ip_address for network_interface in self.network_interfaces
                if network_interface.public_ip_address]

    @property
    def vpc_id(self) -> Optional[str]:
        if self.vpc:
            return self.vpc.vpc_id
        return None

    @property
    def vpc_name(self) -> Optional[str]:
        if self.vpc:
            return self.vpc.name
        return None

    @property
    def vpc(self) -> Optional['Vpc']:
        if self._has_eni:
            return self.network_interfaces[0].subnet.vpc  # An instance can only have ENI's from same VPC
        return None

    @property
    def subnets(self) -> List[Subnet]:
        return [network_interface.subnet for network_interface in self.network_interfaces]

    @property
    def route_tables(self) -> List[RouteTable]:
        return [subnet.route_table for subnet in self.subnets]

    @property
    def routes(self) -> List[Route]:
        return [route for route_table in self.route_tables for route in route_table.routes]

    @property
    def is_inbound_public(self) -> bool:
        return any(x for x in self.network_interfaces if x.is_inbound_public())

    @property
    def is_outbound_public(self) -> bool:
        return any(x for x in self.network_interfaces if x.is_outbound_public())

    @property
    def outbound_connections(self) -> List[ConnectionDetail]:
        return [connection for network_interface in self.network_interfaces for connection in
                network_interface.outbound_connections]

    @property
    def inbound_connections(self) -> List[ConnectionDetail]:
        return [connection for network_interface in self.network_interfaces for connection in
                network_interface.inbound_connections]

    @property
    def owner(self):
        if self._has_eni:
            return self.network_interfaces[0].owner
        return None

    @property
    def security_groups(self) -> Set[SecurityGroup]:
        return {sg for eni in self.network_interfaces for sg in eni.security_groups}

    @property
    def security_groups_ids(self) -> List[str]:
        return [sg.security_group_id for sg in self.security_groups]

    @property
    def subnet_ids(self) -> List[str]:
        return [eni.subnet_id for eni in self.network_interfaces]

    @property
    def _has_eni(self) -> bool:
        return len(self.network_interfaces) > 0
