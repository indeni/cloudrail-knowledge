import functools
import itertools
import logging
from typing import Set, List, Optional, Tuple

from netaddr import IPNetwork, IPSet

from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import IEcsInstance, EcsTaskDefinition
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.route import RouteTargetType, Route
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRouteState, TransitGatewayRoute, TransitGatewayRouteType
from cloudrail.knowledge.utils.utils import is_subset, compare_prefix_length, \
    has_intersection, is_ip_address, normalize_port_range, \
    get_all_ports_range, is_port_in_range


def calculate_allowed_ports(source_eni: NetworkInterface, dest_eni: NetworkInterface,
                            transit_gateways: List[TransitGateway], ports_restrictions: List[int] = None) -> Set[int]:
    if _is_cross_vpc_route_able(source_eni.subnet, dest_eni, transit_gateways):
        ports = _get_ports_allowed_by_security_group(source_eni, dest_eni, ports_restrictions)
        ports = _reduce_allowed_ports_for_nodes_by_acls(source_eni, dest_eni, ports)
        result = set()
        for port_pair in ports:
            result.update(normalize_port_range_to_set(port_pair[0], port_pair[1]))
        return result

    return set()


def _is_cross_vpc_route_able(src_subnet: Subnet, dest_eni: NetworkInterface,
                             transit_gateways: List[TransitGateway]) -> bool:
    if src_subnet.vpc_id == dest_eni.vpc_id:
        # Same VPC nodes are routable by 'local' route
        return True

    for ip in dest_eni.private_ip_addresses:
        route = _get_route_table_relevant_route(src_subnet.route_table.routes, ip)
        if not route:
            continue

        if route.target_type == RouteTargetType.VPC_PEERING_ID and \
                dest_eni.vpc_id in [route.peering_connection.requester_vpc_info.vpc_id, route.peering_connection.accepter_vpc_info.vpc_id]:
            # Check if routable by 'local' route
            if any(x for x in dest_eni.private_ip_addresses if
                   is_subset(x, route.target)):
                return True

        # Check if routable by instance-id redirection
        dest_instance_id: Optional[str] = None
        if dest_eni.owner and isinstance(dest_eni.owner, Ec2Instance):
            dest_instance_id = dest_eni.owner.instance_id
        if route.target_type == RouteTargetType.INSTANCE_ID and dest_instance_id and route.destination == dest_instance_id:
            return True

        # Check if routable by network-interface-id redirection
        if route.target_type == RouteTargetType.NETWORK_INTERFACE_ID and dest_eni.eni_id == route.destination:
            return True

        # Check if routable via transit-gateway-id
        if route.target_type == RouteTargetType.TRANSIT_GATEWAY_ID:
            transit_gateway = next(x for x in transit_gateways if x.tgw_id == route.target)

            route_tables = (rt for rt in transit_gateway.route_tables if any(association for association in rt.associations
                                                                             if src_subnet.subnet_id in association.attachment.subnet_ids))

            for route_table in route_tables:
                route = _get_tgw_relevant_route(route_table.routes, ip)
                if route.state == TransitGatewayRouteState.ACTIVE:
                    return True

    return False


def _get_tgw_relevant_route(routes: List[TransitGatewayRoute], ip: str) -> TransitGatewayRoute:
    """
    Gets the relevant Transit-Gateway-Route-Table route for the destination ip as described in
    `Route Evaluation Order <https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html#tgw-routing-overview>`_
    """
    most_specific_routes: List[TransitGatewayRoute] = None
    for route in routes:
        if is_subset(ip, route.destination_cidr_block):
            if not most_specific_routes:
                most_specific_routes = [route]
            else:
                if compare_prefix_length(most_specific_routes[0].destination_cidr_block, route.destination_cidr_block) == 1:
                    most_specific_routes = [route]
                elif compare_prefix_length(most_specific_routes[0].destination_cidr_block, route.destination_cidr_block) == 0:
                    most_specific_routes.append(route)

    if len(most_specific_routes) == 1:
        return most_specific_routes[0]

    static_route = next((x for x in most_specific_routes if x.route_type == TransitGatewayRouteType.STATIC))
    if static_route:
        return static_route

    # TODO: Among propagated routes, VPC CIDRs have a higher precedence than Direct Connect gateways than Site-to-Site VPN
    return most_specific_routes[0]


def _get_ports_allowed_by_security_group(src_eni: NetworkInterface,
                                         dest_eni: NetworkInterface,
                                         ports_restrictions: List[int] = None) \
        -> List[Tuple[int, int]]:
    ports: List[Tuple[int, int]] = []
    for src_sg in src_eni.security_groups:
        for dst_sg in dest_eni.security_groups:
            for src_outbound_permission in src_sg.outbound_permissions:
                for dst_inbound_permission in dst_sg.inbound_permissions:
                    if src_outbound_permission.is_match(dst_inbound_permission):
                        allowed_ports = get_overlapping_ports(
                            src_outbound_permission.get_ports_range(),
                            dst_inbound_permission.get_ports_range())
                        if allowed_ports:
                            allowed_ports = [allowed_ports]
                        if ports_restrictions and allowed_ports:
                            allowed_ports = intersect_port_ranges(allowed_ports, convert_port_set_to_range_tuples(set(ports_restrictions)))
                        if ports == get_all_ports_range():
                            return ports
                        if allowed_ports is not None:
                            ports = add_port_ranges(ports, allowed_ports)
    return ports


def is_ecs_network_configurations_contains_ports(ecs_instance: IEcsInstance, ports: Set[int]) -> bool:
    task_def: EcsTaskDefinition = ecs_instance.get_task_definition()
    return task_def and any(port_map.container_port in ports for container_def in task_def.container_definitions
                            for port_map in container_def.port_mappings)


def _reduce_allowed_ports_for_nodes_by_acls(src_eni: NetworkInterface,
                                            dest_eni: NetworkInterface,
                                            allowed_ports: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not allowed_ports or src_eni.subnet_id == dest_eni.subnet_id:
        return allowed_ports

    src_acl_rules = src_eni.subnet.network_acl.outbound_rules
    dest_acl_rules = dest_eni.subnet.network_acl.inbound_rules

    acl_dest_allowed_ports = []
    for dest_ip in dest_eni.private_ip_addresses:
        filtered_ports = _reduce_allowed_ports_for_ip_address_by_acls(src_acl_rules, dest_ip, allowed_ports)
        acl_dest_allowed_ports = add_port_ranges(acl_dest_allowed_ports, filtered_ports)

    acl_src_allowed_ports = []
    for src_ip in src_eni.private_ip_addresses:
        filtered_ports = _reduce_allowed_ports_for_ip_address_by_acls(dest_acl_rules, src_ip, allowed_ports)
        acl_src_allowed_ports = add_port_ranges(acl_src_allowed_ports, filtered_ports)

    filtered_ports = intersect_port_ranges(acl_dest_allowed_ports, acl_src_allowed_ports)

    return filtered_ports


def _reduce_allowed_ports_for_ip_address_by_acls(rules: List[NetworkAclRule], ip_address: str, allowed_ports: List[Tuple[int, int]]) -> \
        List[Tuple[int, int]]:
    final_allowed_ports = allowed_ports.copy()
    entries: List[NetworkAclRule] = [rule for rule in rules if has_intersection(rule.cidr_block, ip_address)]
    final_allowed_ports = _reduce_ports_by_network_acl_rules(entries, final_allowed_ports)
    return final_allowed_ports


def _reduce_ports_by_network_acl_rules(entries: List[NetworkAclRule], allowed_ports: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    nacl_allowed_ports = []
    entries.sort(key=lambda x: x.rule_number)
    for entry in entries:
        port_range = [(entry.from_port, entry.to_port)]
        if nacl_allowed_ports and port_range:
            port_range = remove_port_ranges(port_range, nacl_allowed_ports)
        if entry.rule_action == RuleAction.DENY and port_range:
            allowed_ports = remove_port_ranges(allowed_ports, port_range)
        elif port_range:
            nacl_allowed_ports = add_port_ranges(nacl_allowed_ports, port_range)
        if not allowed_ports:
            return allowed_ports
    allowed_ports = intersect_port_ranges(allowed_ports, nacl_allowed_ports)
    return allowed_ports


def _get_route_table_relevant_route(routes: List[Route], ip: str) -> Route:
    """
    Gets the relevant VPC Route-Table route for the destination ip as described in
    `Route Evaluation Order <https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html#tgw-routing-overview>`_
    """
    local_route = next(route for route in routes if route.target == 'local')
    if is_subset(ip, local_route.destination):
        return local_route

    most_specific_route: Route = None
    for route in routes:
        if is_ip_address(ip) and is_subset(ip, route.target):
            if not most_specific_route or \
                    compare_prefix_length(most_specific_route.target, route.target) == -1:
                most_specific_route = route

    return most_specific_route


def reduce_allowed_ports_for_cidr_block_by_acls(rules: List[NetworkAclRule], cidr_block: str, allowed_ports: List[Tuple[int, int]],
                                                strict_mode: bool) -> List[Tuple[int, int]]:
    # TODO: add config for strict mode?
    if not strict_mode:
        return _reduce_allowed_ports_for_ip_address_by_acls(rules, str(IPNetwork(cidr_block)), allowed_ports)
    result: Set = set()
    for port in allowed_ports:
        deny_blocks: IPSet = IPSet()
        entries: List[NetworkAclRule] = [x for x in rules
                                         if is_port_in_range((x.from_port, x.to_port), port)
                                         and has_intersection(cidr_block, x.cidr_block)]
        for entry in entries:
            if any(x for x in deny_blocks.iter_cidrs() if is_subset(entry.cidr_block, str(x))):
                continue

            if entry.rule_action == RuleAction.ALLOW:
                result.add(port)
                break
            else:
                deny_blocks = deny_blocks | IPSet([entry.cidr_block])

    return result


def add_port_range(port_ranges: List[Tuple[int, int]], new_port_range: Tuple[int, int]):
    new_list = []
    index = 0
    start_port = None
    end_port = None
    in_match = None
    while index <= len(port_ranges) - 1:
        port_range = port_ranges[index]
        max_start = max(port_range[0], new_port_range[0])
        min_end = min(port_range[1], new_port_range[1])
        if max_start <= min_end:
            start_port = min(port_range[0], new_port_range[0])
            end_port = max(port_range[1], new_port_range[1])
            in_match = True
            index = index + 1
            while index <= len(port_ranges) - 1:
                port_range = port_ranges[index]
                if in_match:
                    if port_range[0] > end_port:
                        new_list.append((start_port, end_port))
                        new_list.append(port_range)
                        in_match = False
                    else:
                        if port_range[1] < end_port:
                            pass
                        else:
                            in_match = False
                            new_list.append((start_port, port_range[1]))
                else:
                    new_list.append(port_range)
                index = index + 1
        else:
            new_list.append(port_range)
            index = index + 1
    if in_match:
        new_list.append((start_port, end_port))
    found_index = None
    if in_match is None:
        for index, port_range in enumerate(new_list):
            if port_range[0] > new_port_range[1]:
                found_index = index
                break
        if found_index:
            new_list.insert(index, new_port_range)
        elif new_list and new_list[0][0] > new_port_range[0]:
            new_list.insert(0, new_port_range)
        else:
            new_list.append(new_port_range)

    index = 0
    while index <= len(new_list) - 2:
        port_range = new_list[index]
        next_port_range = new_list[index + 1]
        if port_range[1] + 1 == next_port_range[0]:
            new_list.remove(port_range)
            new_list.remove(next_port_range)
            new_list.insert(index, (port_range[0], next_port_range[1]))
        else:
            index = index + 1
    return new_list


def add_port_ranges(port_ranges: List[Tuple[int, int]], new_port_ranges: List[Tuple[int, int]]):
    new_list = port_ranges
    new_list.sort()
    for new_port_range in new_port_ranges:
        new_list = add_port_range(new_list, new_port_range)
        new_list.sort()
    return new_list


def remove_port_ranges(port_ranges: List[Tuple[int, int]], new_port_ranges: List[Tuple[int, int]]):
    new_list = port_ranges
    new_list.sort()
    for new_port_range in new_port_ranges:
        new_list = remove_port_range(new_list, new_port_range)
        new_list.sort()
    return new_list


def remove_port_range(port_ranges: List[Tuple[int, int]], new_port_range: Tuple[int, int]):
    new_list = []
    index = 0
    while index <= len(port_ranges) - 1:
        port_range = port_ranges[index]
        max_start = max(port_range[0], new_port_range[0])
        min_end = min(port_range[1], new_port_range[1])
        if max_start <= min_end:
            if port_range[0] < new_port_range[0]:
                new_list.append((port_range[0], new_port_range[0] - 1))
            if port_range[1] > new_port_range[1]:
                new_list.append((new_port_range[1] + 1, port_range[1]))
                new_list.extend(port_ranges[index + 1:])
                return new_list
            else:
                index = index + 1
                while index <= len(port_ranges) - 1:
                    port_range = port_ranges[index]
                    if port_range[1] <= new_port_range[1]:
                        index = index + 1
                    else:
                        new_list.append((max(port_range[0], new_port_range[1] + 1), port_range[1]))
                        new_list.extend(port_ranges[index + 1:])
                        return new_list
                break
        new_list.append(port_range)
        index = index + 1
    return new_list


def intersect_port_range(port_ranges: List[Tuple[int, int]], new_port_range: Tuple[int, int]):
    new_list = []
    index = 0
    while index <= len(port_ranges) - 1:
        port_range = port_ranges[index]
        max_start = max(port_range[0], new_port_range[0])
        min_end = min(port_range[1], new_port_range[1])
        if max_start <= min_end:
            new_list.append((max_start, min_end))
        if port_range[1] > new_port_range[1]:
            break
        index = index + 1
    return new_list


def intersect_port_ranges(port_ranges: List[Tuple[int, int]], new_port_ranges: List[Tuple[int, int]]):
    result = []
    for new_port_range in new_port_ranges:
        result.extend(intersect_port_range(port_ranges, new_port_range))
    result.sort()
    return result


def is_all_ports(port_range_tuple: Tuple[int, int]) -> bool:
    return port_range_tuple[0] == 0 and port_range_tuple[1] == 65535


@functools.lru_cache(maxsize=None)
def normalize_port_range_to_set(from_port: int, to_port: int) -> Set[int]:
    normalized_port_range = normalize_port_range(from_port, to_port)
    return set(range(normalized_port_range[0], normalized_port_range[1] + 1))


def convert_port_set_to_range_tuples(ports: set) -> List[Tuple[int, int]]:
    if ports == get_all_ports() or len(ports) == 65536:
        return [(0, 65535)]
    if ports is None:
        return []
    port_list = list(ports)
    port_list.sort()
    return [(t[0][1], t[-1][1]) for t in
            (tuple(g[1]) for g in itertools.groupby(enumerate(port_list), lambda x: x[0] - x[1]))]


@functools.lru_cache(maxsize=None)
def get_all_ports():
    all_ports = set(range(0, 65535))
    return all_ports


def get_port_by_engine(engine: str) -> int:
    if engine.startswith('aurora'):
        return 3306
    if engine == 'mariadb':
        return 3306
    if engine == 'mysql':
        return 3306
    if engine.startswith('oracle'):
        return 1521
    if engine == 'postgres':
        return 5432
    if engine.startswith('sqlserver'):
        return 1433

    logging.warning(f'Cannot infer port from engine {engine}')
    return None


@functools.lru_cache(maxsize=None)
def get_overlapping_ports(first_range: Tuple[int, int], second_range: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    first_range = normalize_port_range(first_range[0], first_range[1])
    second_range = normalize_port_range(second_range[0], second_range[1])
    max_start = max(first_range[0], second_range[0])
    min_end = min(first_range[1], second_range[1])
    if min_end - max_start == 65535:
        return get_all_ports_range()
    if max_start > min_end:
        return None
    else:
        return max_start, min_end
