from abc import abstractmethod
from typing import List, Dict, Optional, Set
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.gcp_connection_evaluator import GcpConnectionEvaluator
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.constants.known_ports import KnownPorts
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessVpcPortRule(GcpBaseRule):

    def __init__(self, port: KnownPorts) -> None:
        self.port = port

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.get_all_network_entities())

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for network_entity in env_context.get_all_network_entities():
            firewalls: Set[GcpComputeFirewall] = GcpConnectionEvaluator.firewalls_allowing_incoming_public_conns_on_port(network_entity, self.port)
            if firewalls:
                forwarding_rules = self.conns_forwarding_on_port(network_entity, self.port)
                public_ip_addresses = network_entity.public_ip_addresses
                for firewall in firewalls:
                    if public_ip_addresses and forwarding_rules:
                        for rule in forwarding_rules:
                            issues.append(
                                Issue(
                                    f"The {network_entity.get_type()} `{network_entity.get_friendly_name()}` "
                                    f"with one of the public IP addresses `{', ' .join(public_ip_addresses)}` "
                                    f"and via load balancer `{rule.get_friendly_name()}"
                                    f"is reachable from the Internet via {self.port.name} port",
                                    network_entity,
                                    firewall))
                    elif public_ip_addresses and not forwarding_rules:
                        issues.append(
                                Issue(
                                    f"The {network_entity.get_type()} `{network_entity.get_friendly_name()}` "
                                    f"with one of the public IP addresses `{', ' .join(public_ip_addresses)}` "
                                    f"is reachable from the Internet via {self.port.name} port",
                                    network_entity,
                                    firewall))
                    elif forwarding_rules and not public_ip_addresses:
                        for rule in forwarding_rules:
                            issues.append(
                                Issue(
                                    f"The {network_entity.get_type()} `{network_entity.get_friendly_name()}` "
                                    f"exposed via load balancer `{rule.get_friendly_name()}` "
                                    f"is reachable from the Internet via {self.port.name} port",
                                    network_entity,
                                    firewall))
        return issues

    @staticmethod
    def conns_forwarding_on_port(network_resource: NetworkEntity, port: int) -> Optional[GcpComputeForwardingRule]:
        return [rule for rule in network_resource.forwarding_rules
                if network_resource.self_link in rule.target_pool.instances
                and port in rule.port_range]

class PublicAccessVpcSshPortRule(PublicAccessVpcPortRule):

    def get_id(self) -> str:
        return 'car_vpc_not_publicly_accessible_ssh'

    def __init__(self):
        super().__init__(KnownPorts.SSH)

class PublicAccessVpcRdpPortRule(PublicAccessVpcPortRule):

    def get_id(self) -> str:
        return 'car_vpc_not_publicly_accessible_rdp'

    def __init__(self):
        super().__init__(KnownPorts.RDP)
