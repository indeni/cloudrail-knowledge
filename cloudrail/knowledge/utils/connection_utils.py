from typing import Optional, List

from cloudrail.knowledge.context.connection import ConnectionType, PublicConnectionDetail, PortConnectionProperty, PrivateConnectionDetail
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRulePropertyType, SecurityGroupRule
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.utils.utils import is_subset, is_port_in_range


def get_allowing_indirect_public_access_on_ports(network_entity: NetworkEntity, ports: List[int]) -> Optional[IndirectPublicConnectionData]:
    for eni in network_entity.network_resource.network_interfaces:
        for inbound_connection in eni.inbound_connections:
            if isinstance(inbound_connection, PrivateConnectionDetail) and \
                    isinstance(inbound_connection.connection_property, PortConnectionProperty):
                if any(x for x in inbound_connection.target_instance.inbound_connections if isinstance(x, PublicConnectionDetail)):
                    if isinstance(inbound_connection.target_instance, NetworkInterface):
                        target_instance_sg_ids = [sg.security_group_id for sg in inbound_connection.target_instance.security_groups]
                        return \
                            IndirectPublicConnectionData(_get_security_group_allows_private_inbound_connection_on_port(
                                eni.security_groups, ports, target_instance_sg_ids,
                                inbound_connection.target_instance.private_ip_addresses), inbound_connection.target_instance)
    return None


def get_allowing_public_access_on_ports(network_entity: NetworkEntity, ports: List[int]) -> Optional[SecurityGroup]:
    for eni in network_entity.network_resource.network_interfaces:
        for inbound_connection in eni.inbound_connections:
            if inbound_connection.connection_type is ConnectionType.PUBLIC:
                connection_cidr = inbound_connection.connection_property.cidr_block
                security_group = _get_security_group_allows_public_inbound_connection_on_port(eni.security_groups, ports, connection_cidr)
                if security_group:
                    return security_group

    return None


def _get_security_group_allows_public_inbound_connection_on_port(security_groups: List[SecurityGroup], ports: List[int], cidr: str) \
        -> Optional[SecurityGroup]:
    for security_group in security_groups:
        for inbound_permission in security_group.inbound_permissions:
            inbound_port_range = (inbound_permission.from_port, inbound_permission.to_port)
            if inbound_permission.property_type == SecurityGroupRulePropertyType.IP_RANGES and \
                    is_subset(cidr, inbound_permission.property_value) and \
                    any(is_port_in_range(inbound_port_range, port) for port in ports):
                return security_group
    return None


def _get_security_group_allows_private_inbound_connection_on_port(src_security_groups: List[SecurityGroup], ports: List[int],
                                                                  dest_security_group_ids: List[str], dest_ip_addresses: List[str]) \
        -> Optional[SecurityGroup]:
    for src_security_group in src_security_groups:
        for dest_security_group_id in dest_security_group_ids:
            for inbound_permission in src_security_group.inbound_permissions:
                if any(port for port in ports if is_port_in_range((inbound_permission.from_port, inbound_permission.to_port), port)):
                    if _is_security_group_rule_permissive(inbound_permission, dest_security_group_id, dest_ip_addresses):
                        return src_security_group
    return None


def _is_security_group_rule_permissive(source_permissions: SecurityGroupRule, destination_sg_id: Optional[str], dest_ip_addresses: List[str]) \
        -> bool:
    if source_permissions.property_type == SecurityGroupRulePropertyType.SECURITY_GROUP_ID and destination_sg_id:
        return source_permissions.property_value == destination_sg_id
    if source_permissions.property_type == SecurityGroupRulePropertyType.IP_RANGES:
        ip_ranges = source_permissions.property_value
        return any(ip_address for ip_address in dest_ip_addresses if is_subset(ip_address, ip_ranges))
    return False


def get_allowing_public_access_portless(network_entity: NetworkEntity) -> Optional[SecurityGroup]:
    for eni in network_entity.network_resource.network_interfaces:
        for inbound_connection in eni.inbound_connections:
            if inbound_connection.connection_type is ConnectionType.PUBLIC and \
                    isinstance(inbound_connection.connection_property, PortConnectionProperty):
                connection_cidr = inbound_connection.connection_property.cidr_block
                security_group = _get_security_group_allows_public_inbound_connection_portless(eni.security_groups, connection_cidr)
                return security_group

    return None


def _get_security_group_allows_public_inbound_connection_portless(security_groups: List[SecurityGroup], cidr: str) -> Optional[SecurityGroup]:
    for security_group in security_groups:
        for inbound_permission in security_group.inbound_permissions:
            if inbound_permission.property_type == SecurityGroupRulePropertyType.IP_RANGES \
                    and is_subset(cidr, inbound_permission.property_value):
                return security_group
    return None
