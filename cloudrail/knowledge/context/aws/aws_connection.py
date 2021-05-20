from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Set

from dataclasses_json import DataClassJsonMixin

from cloudrail.knowledge.utils.utils import hash_list


@dataclass
class PolicyEvaluation(DataClassJsonMixin):
    resource_allowed_actions: Set[str] = field(default_factory=set)
    resource_denied_actions: Set[str] = field(default_factory=set)

    identity_allowed_actions: Set[str] = field(default_factory=set)
    identity_denied_actions: Set[str] = field(default_factory=set)

    permission_boundary_applied: bool = False
    permission_boundary_allowed_actions: Set[str] = field(default_factory=set)
    permission_boundary_denied_actions: Set[str] = field(default_factory=set)


class ConnectionDirectionType(Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'


class ConnectionType(Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'


class ConnectionProperty:
    pass


class PolicyConnectionProperty(ConnectionProperty):
    def __init__(self, policy_evaluation: List[PolicyEvaluation]):
        self.policy_evaluation = policy_evaluation


class PortConnectionProperty(ConnectionProperty):
    def __init__(self, ports: List[Tuple[int, int]], cidr_block: str, ip_protocol_type: str):
        self.ports: List[Tuple[int, int]] = ports  # todo - should be only tuple
        self.cidr_block: str = cidr_block
        self.ip_protocol_type: str = ip_protocol_type

    def __eq__(self, o: object) -> bool:
        if isinstance(o, PortConnectionProperty):
            return len(o.ports) == len(self.ports) and \
                   all(o.ports[index][0] == self.ports[index][0] and o.ports[index][1] == self.ports[index][1]
                       for index in range(len(self.ports))) and \
                   self.cidr_block == o.cidr_block and \
                   self.ip_protocol_type == o.ip_protocol_type
        return False

    def __hash__(self) -> int:
        return hash_list([hash_list(self.ports or []), self.cidr_block, self.ip_protocol_type])


@dataclass
class ConnectionDetail:
    connection_type: ConnectionType = field(init=False)
    connection_property: ConnectionProperty
    connection_direction_type: ConnectionDirectionType


class ConnectionInstance:
    def __init__(self):
        self.inbound_connections: Set[ConnectionDetail] = set()
        self.outbound_connections: Set[ConnectionDetail] = set()

    def add_private_inbound_conn(self, conn: ConnectionProperty, target_instance: 'ConnectionInstance') -> None:
        conn_detail: ConnectionDetail = PrivateConnectionDetail(conn, ConnectionDirectionType.INBOUND, target_instance)
        self.inbound_connections.add(conn_detail)

    def add_public_inbound_conn(self, conn: ConnectionProperty) -> None:
        conn_detail: ConnectionDetail = PublicConnectionDetail(conn, ConnectionDirectionType.INBOUND)
        self.inbound_connections.add(conn_detail)

    def add_private_outbound_conn(self, conn: ConnectionProperty, target_instance) -> None:
        conn_detail: ConnectionDetail = PrivateConnectionDetail(conn, ConnectionDirectionType.OUTBOUND, target_instance)
        self.outbound_connections.add(conn_detail)

    def add_public_outbound_conn(self, conn: ConnectionProperty) -> None:
        conn_detail: ConnectionDetail = PublicConnectionDetail(conn, ConnectionDirectionType.OUTBOUND)
        self.outbound_connections.add(conn_detail)

    def is_inbound_public(self) -> bool:
        return any(x for x in self.inbound_connections if x.connection_type == ConnectionType.PUBLIC)

    def is_outbound_public(self) -> bool:
        return any(x for x in self.outbound_connections if x.connection_type == ConnectionType.PUBLIC)


@dataclass
class PrivateConnectionDetail(ConnectionDetail):
    target_instance: ConnectionInstance
    connection_type = ConnectionType.PRIVATE

    def __hash__(self) -> int:
        return hash((self.connection_type,
                     self.connection_direction_type,
                     self.connection_property,
                     self.target_instance))


@dataclass
class PublicConnectionDetail(ConnectionDetail):
    connection_type = ConnectionType.PUBLIC

    def __hash__(self) -> int:
        return hash((self.connection_type, self.connection_direction_type, self.connection_property))
