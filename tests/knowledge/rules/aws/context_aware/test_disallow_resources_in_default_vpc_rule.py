import unittest

from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.disallow_resources_in_default_vpc_rule import DisallowResourcesInDefaultVpcRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestDisallowEc2ClassicModeRule(unittest.TestCase):
    def setUp(self):
        self.rule = DisallowResourcesInDefaultVpcRule()

    def test_disallow_resources_in_default_vpc_rule_fail(self):
        # Arrange
        ec2 = create_empty_entity(Ec2Instance)
        vpc = create_empty_entity(Vpc)
        vpc.is_default = True
        network_interface = create_empty_entity(NetworkInterface)
        subnet = create_empty_entity(Subnet)
        network_interface.subnet = subnet
        subnet.vpc = vpc
        ec2.network_resource.network_interfaces.append(network_interface)
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(ec2, result.issues[0].exposed)
        self.assertEqual(ec2, result.issues[0].violating)

    def test_disallow_resources_in_default_vpc_rule_pass(self):
        # Arrange
        ec2 = create_empty_entity(Ec2Instance)
        vpc = create_empty_entity(Vpc)
        vpc.is_default = False
        network_interface = create_empty_entity(NetworkInterface)
        subnet = create_empty_entity(Subnet)
        network_interface.subnet = subnet
        subnet.vpc = vpc
        ec2.network_resource.network_interfaces.append(network_interface)
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
