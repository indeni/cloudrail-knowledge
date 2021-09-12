import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.context_aware.ensure_no_unused_security_groups_rule import EnsureNoUnusedSecurityGroups
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureNoUnusedSecurityGroups(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNoUnusedSecurityGroups()

    def test_car_unused_security_group_fail(self):
        # Arrange
        security_group_1: SecurityGroup = create_empty_entity(SecurityGroup)
        security_group_2: SecurityGroup = create_empty_entity(SecurityGroup)
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.add_security_group(security_group_1)
        network_interface.owner = ec2
        ec2.network_resource.network_interfaces.append(network_interface)
        security_group_2.iac_state = IacState(address='address',
                                              action=TerraformActionType.NO_OP,
                                              resource_metadata=None,
                                              is_new=False)
        context = AwsEnvironmentContext(ec2s=[ec2], network_interfaces=AliasesDict(network_interface),
                                        security_groups=AliasesDict(security_group_1, security_group_2))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_car_unused_security_group__no_unused_sg__pass(self):
        # Arrange
        security_group_1: SecurityGroup = create_empty_entity(SecurityGroup)
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.add_security_group(security_group_1)
        network_interface.owner = ec2
        ec2.network_resource.network_interfaces.append(network_interface)
        security_group_1.add_usage(network_interface)
        context = AwsEnvironmentContext(ec2s=[ec2], network_interfaces=AliasesDict(network_interface),
                                        security_groups=AliasesDict(security_group_1))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_car_unused_security_group__unused_sg_is_new__pass(self):
        # Arrange
        security_group_1: SecurityGroup = create_empty_entity(SecurityGroup)
        security_group_2: SecurityGroup = create_empty_entity(SecurityGroup)
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.add_security_group(security_group_1)
        security_group_1.add_usage(network_interface)
        network_interface.owner = ec2
        ec2.network_resource.network_interfaces.append(network_interface)
        security_group_2.iac_state = IacState(address='address',
                                              action=TerraformActionType.CREATE,
                                              resource_metadata=None,
                                              is_new=True)
        context = AwsEnvironmentContext(ec2s=[ec2], network_interfaces=AliasesDict(network_interface),
                                        security_groups=AliasesDict(security_group_1, security_group_2))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
