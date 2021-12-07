from typing import Set, List
from cloudrail.knowledge.context.connection import ConnectionType, PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import FirewallRuleAction, GcpComputeFirewallDirection, GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import NetworkEntity, GcpConnection
from cloudrail.knowledge.utils.utils import is_public_ip_range


class GcpConnectionBuilder(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext):
        network_entities = ctx.get_all_network_entities()
        function_pool = [
            IterFunctionData(self._assign_port_connections, network_entities, ()),
        ]

        super().__init__(function_pool, context=None)

    ## Evaluation of GCP connections, fowllowing GCP doc: https://cloud.google.com/vpc/docs/firewalls
    def _assign_port_connections(self, network_entity: NetworkEntity):
        connections_set: List[GcpConnection] = []
        enforced_firewalls: List[GcpComputeFirewall] = [firewall for firewall in network_entity.firewalls if not firewall.disabled]
        for firewall in enforced_firewalls:
            connection_direction = ConnectionDirectionType.INBOUND if firewall.direction == GcpComputeFirewallDirection.INGRESS else ConnectionDirectionType.OUTBOUND
            for cidr in firewall.firewall_ip_ranges:
                connection_type = ConnectionType.PUBLIC if is_public_ip_range(cidr) else ConnectionType.PRIVATE
                for rule in firewall.allow:
                    connections_set.append(GcpConnection(connection_type=connection_type,
                                                         connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                         connection_direction_type=connection_direction,
                                                         firewall_action=FirewallRuleAction.ALLOW,
                                                         priority=firewall.priority,
                                                         firewall=firewall))
                for rule in firewall.deny:
                    connections_set.append(GcpConnection(connection_type=connection_type,
                                                         connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                         connection_direction_type=connection_direction,
                                                         firewall_action=FirewallRuleAction.DENY,
                                                         priority=firewall.priority,
                                                         firewall=firewall))
        connections_set = sorted(connections_set, key=lambda rule: rule.priority)
        connections_list = self._filter_conns_by_priority_and_action(connections_set)
        inbound_conns: List[GcpConnection] = [conn for conn in connections_list if conn.connection_direction_type == ConnectionDirectionType.INBOUND]
        outbound_conns: List[GcpConnection] = [conn for conn in connections_list if conn.connection_direction_type == ConnectionDirectionType.OUTBOUND]
        network_entity.inbound_connections = sorted(inbound_conns, key=lambda conn: conn.priority)
        network_entity.outbound_connections = sorted(outbound_conns, key=lambda conn: conn.priority)

    @staticmethod
    def _filter_conns_by_priority_and_action(connections_set: Set[GcpConnection]) -> List[GcpConnection]:
        connections_list: List[GcpConnection] = []
        for connection in connections_set:
            if not any(connection.compare_conn(list_con) for list_con in connections_list):
                conns_with_same_priority = [list_con for list_con in connections_set if list_con.priority == connection.priority and connection.compare_conn(list_con)]
                if len(conns_with_same_priority) > 1:
                    connections_list.extend(sorted(conns_with_same_priority, key=lambda conn: conn.firewall_action == FirewallRuleAction.DENY))
                else:
                    connections_list.append(connection)
        return connections_list
