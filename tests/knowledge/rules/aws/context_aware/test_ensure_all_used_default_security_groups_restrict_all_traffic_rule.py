import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.ensure_all_used_default_security_groups_restrict_all_traffic_rule import \
    EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestDisallowEc2ClassicModeRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule()

    def test_ensure_all_used_default_security_groups_restrict_all_traffic_rule_fail(self):
        # Arrange
        vpc: Vpc = create_empty_entity(Vpc)

        security_group_rule: SecurityGroupRule = create_empty_entity(SecurityGroupRule)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        security_group.is_default = True
        security_group.inbound_permissions.append(security_group_rule)
        security_group.vpc = vpc
        ec2_0: Ec2Instance = create_empty_entity(Ec2Instance)
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.add_security_group(security_group)
        network_interface.owner = ec2_0

        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces.append(network_interface)

        context = AwsEnvironmentContext(vpcs=AliasesDict(vpc), ec2s=[ec2, ec2_0],
                                        security_groups=AliasesDict(security_group))

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(ec2_0, result.issues[0].exposed)
        self.assertEqual(security_group, result.issues[0].violating)

    def test_ensure_all_used_default_security_groups_restrict_all_traffic_rule_pass(self):
        # Arrange
        vpc: Vpc = create_empty_entity(Vpc)

        security_group_rule: SecurityGroupRule = create_empty_entity(SecurityGroupRule)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        security_group.is_default = False
        security_group.inbound_permissions.append(security_group_rule)
        security_group.vpc = vpc
        ec2_0: Ec2Instance = create_empty_entity(Ec2Instance)
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        network_interface.add_security_group(security_group)
        network_interface.owner = ec2_0

        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.network_resource.network_interfaces.append(network_interface)

        context = AwsEnvironmentContext(vpcs=[vpc], ec2s=[ec2])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
