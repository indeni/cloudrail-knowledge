
import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.connection import PortConnectionProperty
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule import \
    PublicAccessSecurityGroupsAllPortsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.utils.utils import get_all_ports_range


class TestPublicAccessSecurityGroupsAllPortsRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessSecurityGroupsAllPortsRule()

    def test_public_access_security_groups_all_ports_rule_fail(self):
        # Arrange
        context = self._create_violating_context()
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_security_groups_all_ports_rule_pass_non_public(self):
        # Arrange
        context = self._create_violating_context()
        next(iter(context.network_interfaces)).inbound_connections = set()
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_public_access_security_groups_all_ports_rule_pass_not_on_all_ips(self):
        # Arrange
        context = self._create_violating_context()
        inbound_connections = next(iter(context.network_interfaces)).inbound_connections
        list(inbound_connections)[0].connection_property = PortConnectionProperty([get_all_ports_range()], '1.0.0.0/0', 'tcp')
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_public_access_security_groups_all_ports_rule_pass_not_on_all_ports(self):
        # Arrange
        context = self._create_violating_context()
        inbound_connections = next(iter(context.network_interfaces)).inbound_connections
        from_port, to_port = get_all_ports_range()
        list(inbound_connections)[0].connection_property = PortConnectionProperty([(from_port+1, to_port)], '0.0.0.0/0', 'tcp')
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    @staticmethod
    def _create_violating_context():
        ec2 = create_empty_network_entity(Ec2Instance)
        eni = ec2.network_resource.network_interfaces[0]
        eni.add_public_inbound_conn(PortConnectionProperty([get_all_ports_range()], '0.0.0.0/0', 'tcp'))
        security_group = create_empty_entity(SecurityGroup)
        eni.security_groups.append(security_group)
        all_inclusive_sg_rule = create_empty_entity(SecurityGroupRule)
        all_inclusive_sg_rule.from_port = 0
        all_inclusive_sg_rule.to_port = get_all_ports_range()[1]
        all_inclusive_sg_rule.property_type = SecurityGroupRulePropertyType.IP_RANGES
        all_inclusive_sg_rule.property_value = '0.0.0.0/0'
        security_group.inbound_permissions.append(all_inclusive_sg_rule)

        return AwsEnvironmentContext(network_interfaces=AliasesDict(eni), security_groups=AliasesDict(security_group),
                                     security_group_rules=[all_inclusive_sg_rule], ec2s=[ec2])
