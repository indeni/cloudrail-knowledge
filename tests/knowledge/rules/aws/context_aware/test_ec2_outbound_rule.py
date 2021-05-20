import unittest

from cloudrail.knowledge.context.aws.aws_connection import PolicyConnectionProperty, ConnectionDirectionType, PublicConnectionDetail, PrivateConnectionDetail, \
    ConnectionInstance
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.ec2_outbound_rule import Ec2OutboundRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEc2InboundRule(unittest.TestCase):
    def setUp(self):
        self.rule = Ec2OutboundRule()

    @unittest.skip("rule param not supported")
    def test_ec2_outbound_rule_using_public_connection_fail(self):
        # Arrange
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.OUTBOUND)

        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.outbound_connections.add(connection_detail)

        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces.append(network_interface)

        ec2_non_fw: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces[0].owner = ec2_non_fw

        context = EnvironmentContext(ec2s=[ec2, ec2_non_fw])

        # Act
        result = self.rule.run(context, {ParameterType.FIREWALL_EC2: []})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(ec2, result.issues[0].exposed)
        self.assertEqual(ec2, result.issues[0].violating)

    def test_ec2_outbound_rule_using_private_connection_pass(self):
        # Arrange
        connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.OUTBOUND, ConnectionInstance())

        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.outbound_connections.add(connection_detail)

        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces.append(network_interface)

        context = EnvironmentContext(ec2s=[ec2])

        # Act
        result = self.rule.run(context, {ParameterType.FIREWALL_EC2: []})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_ec2_outbound_rule_using_fw_pass(self):
        # Arrange
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.OUTBOUND)

        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.outbound_connections.add(connection_detail)

        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces.append(network_interface)

        ec2_fw: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces[0].owner = ec2_fw

        context = EnvironmentContext(ec2s=[ec2, ec2_fw])

        # Act
        result = self.rule.run(context, {ParameterType.FIREWALL_EC2: [ec2_fw]})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
