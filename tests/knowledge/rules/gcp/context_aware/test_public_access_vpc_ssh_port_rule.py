from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.connection import ConnectionDirectionType, ConnectionType, PortConnectionProperty
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, GcpComputeFirewallAction, FirewallRuleAction, GcpComputeFirewallDirection
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import GcpConnection
from cloudrail.knowledge.context.gcp.resources.networking_config.network_interface import GcpNetworkInterface
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.context_aware.public_access_vpc_port_rule import PublicAccessVpcSshPortRule
from cloudrail.knowledge.utils.port_set import PortSet


class TestPublicAccessVpcSshPortRule(TestCase):
    def setUp(self):
        self.rule = PublicAccessVpcSshPortRule()

    @parameterized.expand(
        [
            ["unrestrict_ssh_access", '0.0.0.0/0', True],
            ["restrict_ssh_access", '10.11.20.5/24', False],
        ]
    )

    def test_public_access_vpc_port_rule(self, unused_name: str, source_range: list, should_alert: bool):
        # Arrange
        compute_instance = create_empty_entity(GcpComputeInstance)
        compute_instance_nics: GcpNetworkInterface = create_empty_entity(GcpNetworkInterface)
        compute_instance_nics.public_ips = ['10.10.130.15/24']
        compute_instance.network_interfaces = [compute_instance_nics]
        firewall: GcpComputeFirewall = create_empty_entity(GcpComputeFirewall)
        network: GcpComputeNetwork = create_empty_entity(GcpComputeNetwork)
        gcp_connection: GcpConnection = create_empty_entity(GcpConnection)
        network.name = 'vpc_network'
        allow_firewall_rule: GcpComputeFirewallAction = create_empty_entity(GcpComputeFirewallAction)
        allow_firewall_rule.action = FirewallRuleAction.ALLOW
        allow_firewall_rule.ports = PortSet([22])
        allow_firewall_rule.protocol = IpProtocol('TCP')
        firewall.allow = [allow_firewall_rule]
        firewall.source_ranges = [source_range]
        firewall.direction = GcpComputeFirewallDirection.INGRESS
        firewall.network = network.name
        firewall.disabled = False
        firewall.priority = 10
        network.firewalls = [firewall]
        gcp_connection.connection_direction_type = ConnectionDirectionType.INBOUND
        gcp_connection.connection_property = PortConnectionProperty(PortSet([22, 22]).port_ranges, source_range, IpProtocol('TCP'))
        gcp_connection.connection_type = ConnectionType.PUBLIC
        gcp_connection.firewall = firewall
        gcp_connection.firewall_action = FirewallRuleAction.ALLOW
        compute_instance.inbound_connections = [gcp_connection]
        context = GcpEnvironmentContext(compute_instances=[compute_instance],
                                        compute_firewalls=[firewall],
                                        compute_networks=[network])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
