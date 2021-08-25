import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.network.azure_network_interface import AzureNetworkInterface, IpConfiguration
from cloudrail.knowledge.context.azure.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.network.azure_network_security_group_rule import AzureNetworkSecurityRule, NetworkSecurityRuleActionType
from cloudrail.knowledge.context.azure.network.azure_public_ip import AzurePublicIp
from cloudrail.knowledge.context.azure.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.connection import PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.rules.azure.context_aware.not_publicly_accessible_rule import VirtualMachineNotPubliclyAccessibleSshRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity, add_terraform_state
from cloudrail.knowledge.utils.port_set import PortSet


class TestNotPubliclyAccessible(unittest.TestCase):
    def setUp(self):
        self.rule = VirtualMachineNotPubliclyAccessibleSshRule()

    def test_without_connection(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_with_connection_on_irrelevant_port(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(11, 11)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_with_connection_without_public_ip_address_without_nsg(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence, 'The Virtual Machine `tmp-name` with unknown public IP address is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, public_ip)

    def test_with_connection_with_public_ip_address_without_nsg(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        public_ip.public_ip_address = '1.1.1.1'
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence, 'The Virtual Machine `tmp-name` with public IP address `1.1.1.1` is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, public_ip)

    def test_with_connection_with_nsg_on_network_interface(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        public_ip.public_ip_address = '1.1.1.1'
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]
        network_interface.network_security_group = create_empty_entity(AzureNetworkSecurityGroup)
        nsg_rule = create_empty_entity(AzureNetworkSecurityRule)
        nsg_rule.iac_state = None
        nsg_rule.access = NetworkSecurityRuleActionType.ALLOW
        nsg_rule.direction = ConnectionDirectionType.INBOUND
        nsg_rule.destination_port_ranges = PortSet([22])

        network_interface.network_security_group.network_security_rules = [nsg_rule]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence, 'The Virtual Machine `tmp-name` with public IP address `1.1.1.1` is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, network_interface.network_security_group)

    def test_with_connection_with_nsg_on_network_interface_violating_rule_managed_by_iac(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        public_ip.public_ip_address = '1.1.1.1'
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]
        network_interface.network_security_group = create_empty_entity(AzureNetworkSecurityGroup)
        nsg_rule = create_empty_entity(AzureNetworkSecurityRule)
        nsg_rule.access = NetworkSecurityRuleActionType.ALLOW
        nsg_rule.direction = ConnectionDirectionType.INBOUND
        nsg_rule.destination_port_ranges = PortSet([22])
        add_terraform_state(nsg_rule, 'nsg_rule_address')

        network_interface.network_security_group.network_security_rules = [nsg_rule]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence, 'The Virtual Machine `tmp-name` with NAT rule `nsg_rule_address` is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, nsg_rule)

    def test_with_connection_with_nsg_on_subnet(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        public_ip.public_ip_address = '1.1.1.1'
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)
        network_interface.ip_configurations[0].subnet.network_security_group = create_empty_entity(AzureNetworkSecurityGroup)
        nsg_rule = create_empty_entity(AzureNetworkSecurityRule)
        nsg_rule.iac_state = None
        nsg_rule.access = NetworkSecurityRuleActionType.ALLOW
        nsg_rule.direction = ConnectionDirectionType.INBOUND
        nsg_rule.destination_port_ranges = PortSet([22])

        network_interface.ip_configurations[0].subnet.network_security_group.network_security_rules = [nsg_rule]

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence, 'The Virtual Machine `tmp-name` with public IP address `1.1.1.1` is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, network_interface.ip_configurations[0].subnet.network_security_group)

    def test_with_connection_with_nsg_on_subnet_and_network_interface(self):
        # Arrange
        vm = create_empty_entity(AzureVirtualMachine, name='tmp-name')
        vm.iac_state.address = 'tmp-name'
        network_interface = create_empty_entity(AzureNetworkInterface)
        public_ip = create_empty_entity(AzurePublicIp)
        public_ip.public_ip_address = '1.1.1.1'
        network_interface.ip_configurations = [IpConfiguration('', '', '', [])]
        network_interface.network_security_group = create_empty_entity(AzureNetworkSecurityGroup, name='nic_nsg')
        nsg_rule = create_empty_entity(AzureNetworkSecurityRule)
        nsg_rule.iac_state = None
        nsg_rule.access = NetworkSecurityRuleActionType.ALLOW
        nsg_rule.direction = ConnectionDirectionType.INBOUND
        nsg_rule.destination_port_ranges = PortSet([22])
        network_interface.network_security_group.network_security_rules = [nsg_rule]

        vm.network_interfaces.append(network_interface)
        network_interface.ip_configurations[0].public_ip = public_ip
        network_interface.ip_configurations[0].subnet = create_empty_entity(AzureSubnet)
        network_interface.ip_configurations[0].subnet.network_security_group = create_empty_entity(AzureNetworkSecurityGroup, name='subnet_nsg')
        nsg_rule = create_empty_entity(AzureNetworkSecurityRule)
        nsg_rule.iac_state = None
        nsg_rule.access = NetworkSecurityRuleActionType.ALLOW
        nsg_rule.direction = ConnectionDirectionType.INBOUND
        nsg_rule.destination_port_ranges = PortSet([22])

        network_interface.ip_configurations[0].subnet.network_security_group.network_security_rules = [nsg_rule]

        network_interface.ip_configurations[0].add_public_inbound_conn(
            PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol(IpProtocol.ALL))
        )

        context = AzureEnvironmentContext(virtual_machines=AliasesDict(vm))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].evidence,
                         'The Virtual Machine `tmp-name` with public IP address `1.1.1.1` is reachable from the internet via SSH port')
        self.assertEqual(result.issues[0].violating, network_interface.network_security_group)
