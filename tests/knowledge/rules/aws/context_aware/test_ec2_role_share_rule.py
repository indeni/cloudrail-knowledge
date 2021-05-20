import unittest

from cloudrail.knowledge.context.aws.aws_connection import PublicConnectionDetail, PolicyConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.ec2_role_share_rule import Ec2RoleShareRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEc2RoleShareRule(unittest.TestCase):
    def setUp(self):
        self.rule = Ec2RoleShareRule()

    def test_ec2_role_share_rule_fail(self):
        # Arrange
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)

        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.inbound_connections.add(connection_detail)

        private_ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        private_ec2.iam_profile_id = 'iam_profile_id'

        role: Role = create_empty_entity(Role)
        role.role_name = 'iam_role'
        private_ec2.iam_role = role

        public_ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        public_ec2.iam_profile_id = 'iam_profile_id'
        public_ec2.network_resource.network_interfaces.append(network_interface)

        context = EnvironmentContext(ec2s=[private_ec2, public_ec2])

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_ec2_role_share_rule_pass(self):
        # Arrange
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)

        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.inbound_connections.add(connection_detail)

        private_ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        private_ec2.iam_profile_id = 'iam_profile_id1'

        role: Role = create_empty_entity(Role)
        role.role_name = 'iam_role'
        private_ec2.iam_role = role

        public_ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        public_ec2.iam_profile_id = 'iam_profile_id2'
        public_ec2.network_resource.network_interfaces.append(network_interface)

        context = EnvironmentContext(ec2s=[private_ec2, public_ec2])

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
