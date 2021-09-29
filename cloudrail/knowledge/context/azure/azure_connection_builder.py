from typing import List

from cloudrail.knowledge.context.connection import PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import NetworkSecurityRuleActionType
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.utils.utils import get_all_ports_range, is_public_ip_range, has_intersection, is_valid_cidr_block, \
    generate_random_public_ipv4
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from netaddr import IPSet


class AzureConnectionBuilder(DependencyInvocation):

    def __init__(self, ctx: AzureEnvironmentContext):
        function_pool = [
            ### Public Inbound Connections
            IterFunctionData(self._assign_inbound_public_port_connections, ctx.virtual_machines, ()),

        ]

        super().__init__(function_pool, context=None)

    @classmethod
    def _assign_inbound_public_port_connections(cls, virtual_machine: AzureVirtualMachine):
        for network_interface in virtual_machine.network_interfaces:
            cls._assign_nic_public_connections(network_interface)

    @classmethod
    def _assign_nic_public_connections(cls, nic: AzureNetworkInterface):
        all_ports_range = get_all_ports_range()
        base_conns = [PortConnectionProperty([all_ports_range], '0.0.0.0/0', IpProtocol(IpProtocol.ALL)),
                      PortConnectionProperty([all_ports_range], '::/0', IpProtocol(IpProtocol.ALL))]

        for ip_config in nic.ip_configurations:
            if not ip_config.public_ip:
                continue
            # if 'public_ip_address' is None, then either a public IP was not allocated, or its a new PublicIp resource
            public_ip = ip_config.public_ip.public_ip_address or generate_random_public_ipv4()
            conns = cls._apply_nsg_rules_on_connections(base_conns, nic.network_security_group, public_ip, ip_config.application_security_groups)
            conns = cls._apply_nsg_rules_on_connections(conns, ip_config.subnet.network_security_group, public_ip, ip_config.application_security_groups)
            for conn in conns:
                if is_public_ip_range(conn.cidr_block):
                    ip_config.add_public_inbound_conn(conn)

    @staticmethod
    def _apply_nsg_rules_on_connections(conns: List[PortConnectionProperty], nsg: AzureNetworkSecurityGroup, ip: str, asgs: List[AzureApplicationSecurityGroup]) -> List[PortConnectionProperty]:
        if nsg is None:
            return conns

        nsg.network_security_rules.sort(key=lambda x: x.priority)
        new_conns: List[PortConnectionProperty] = []
        deny_conns: List[PortConnectionProperty] = []
        for rule in nsg.network_security_rules:
            if rule.direction != ConnectionDirectionType.INBOUND:
                continue

            # The values in address_prefixes could also be 'VirtualNetwork'/'AzureLoadBalancer' or a service tag like 'ApiManagement'/'SqlManagement' etc.
            # The above prefixes are not supported.
            # Currently, only supporting '*'/'Internet' which we translate to '0.0.0.0/0' and '::/0',
            # Or CIDR blocks
            rule_source_address_prefixes = [prefix for prefix in rule.source_address_prefixes if is_valid_cidr_block(prefix)]

            if rule.destination_application_security_group_ids:
                if not any(asg.get_id() == asg_id for asg in asgs for asg_id in rule.destination_application_security_group_ids):
                    continue
            else:
                rule_destination_address_prefixes = [prefix for prefix in rule.destination_address_prefixes if is_valid_cidr_block(prefix)]
                if not any(has_intersection(destination_address, ip) for destination_address in rule_destination_address_prefixes):
                    continue

            for conn in conns:
                overlap_ports_range = PortSet(conn.ports).intersection(rule.destination_port_ranges)
                cidrs_overlap_set: IPSet = IPSet([conn.cidr_block]).intersection(IPSet(rule_source_address_prefixes))
                protocol = conn.ip_protocol_type.intersection(rule.protocol)

                is_matched_condition = lambda: overlap_ports_range and cidrs_overlap_set and protocol

                for deny_con in deny_conns:
                    if not is_matched_condition():
                        break
                    overlap_ports_range = overlap_ports_range - deny_con.ports
                    cidrs_overlap_set = cidrs_overlap_set - deny_con.cidr_block

                if not is_matched_condition():
                    break

                if rule.access == NetworkSecurityRuleActionType.DENY:
                    deny_conns.append(PortConnectionProperty(overlap_ports_range, cidrs_overlap_set, protocol))
                else:
                    # Should change PortConnectionProperty to be (PortSet, IPSet, IpProtocol)
                    for overlap_cidr in cidrs_overlap_set.iter_cidrs():
                        new_conns.append(PortConnectionProperty(overlap_ports_range.port_ranges, str(overlap_cidr), protocol))

        return new_conns
