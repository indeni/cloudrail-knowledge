from unittest import skip

from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRulePropertyType

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


# pylint: disable=protected-access
class TestSecurityGroup(AwsContextTest):

    def get_component(self):
        return "security_group"

    @context(module_path="sg-no-vpc-id")
    def test_sg_no_vpc_id(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups
                               if sg.name == 'distinct_name'), None)
        self.assertIsNotNone(security_group)
        self.assertTrue(security_group.vpc.is_default)
        self.assertTrue(security_group.has_description)
        self.assertEqual(len(security_group.inbound_permissions), 0)
        self.assertEqual(len(security_group.outbound_permissions), 0)
        self.assertFalse(security_group.tags)

    @context(module_path="description_on_sg_and_rule")
    def test_description_on_sg_and_rule(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups
                               if sg.name == 'examplerulename'), None)
        self.assertIsNotNone(security_group)
        self.assertTrue(security_group.has_description)
        self.assertEqual(len(security_group.inbound_permissions), 1)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(security_group.inbound_permissions[0].from_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].to_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].property_value, '10.0.0.0/24')
        self.assertTrue(security_group.inbound_permissions[0].has_description)
        self.assertEqual(security_group.outbound_permissions[0].from_port, 0)
        self.assertEqual(security_group.outbound_permissions[0].to_port, 65535)
        self.assertEqual(security_group.outbound_permissions[0].property_value, '0.0.0.0/0')
        self.assertTrue(security_group.outbound_permissions[0].has_description)
        self.assertTrue(security_group.tags)

    @context(module_path="description_only_on_rules")
    def test_description_only_on_rules(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups
                               if sg.name == 'examplerulename'), None)
        self.assertIsNotNone(security_group)
        self.assertFalse(security_group.has_description)
        self.assertEqual(len(security_group.inbound_permissions), 1)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(security_group.inbound_permissions[0].from_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].to_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].property_value, '10.0.0.0/24')
        self.assertTrue(security_group.inbound_permissions[0].has_description)
        self.assertEqual(security_group.outbound_permissions[0].from_port, 0)
        self.assertEqual(security_group.outbound_permissions[0].to_port, 65535)
        self.assertEqual(security_group.outbound_permissions[0].property_value, '0.0.0.0/0')
        self.assertTrue(security_group.outbound_permissions[0].has_description)

    @skip('CR-2519')
    @context(module_path="sg_used_by_ec2")
    def test_sg_used_by_ec2(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups if sg.name == 'distinct_name'), None)
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'Linux Instance'), None)
        sg_used_by = list(security_group._used_by)[0]
        self.assertTrue(isinstance(sg_used_by, NetworkInterface))
        self.assertEqual(sg_used_by.owner, ec2)

        # If NetworkInterface has no owner, then the SG is effectively not used
        sg_used_by.owner = None
        self.assertFalse(security_group.is_used)
        # Resource invalidation has no effect on is_used
        sg_used_by.owner = ec2
        ec2.add_invalidation('some reason')
        self.assertTrue(security_group.is_used)

        ec2.invalidation = set()
        sg_used_by.add_invalidation('some reason')
        self.assertTrue(security_group.is_used)

    @context(module_path="description_only_on_sg")
    def test_description_only_on_sg(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups
                               if sg.name == 'examplerulename'), None)
        self.assertIsNotNone(security_group)
        self.assertTrue(security_group.has_description)
        self.assertEqual(len(security_group.inbound_permissions), 1)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(security_group.inbound_permissions[0].from_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].to_port, 443)
        self.assertEqual(security_group.inbound_permissions[0].property_value, '10.0.0.0/24')
        self.assertFalse(security_group.inbound_permissions[0].has_description)
        self.assertEqual(security_group.outbound_permissions[0].from_port, 0)
        self.assertEqual(security_group.outbound_permissions[0].to_port, 65535)
        self.assertEqual(security_group.outbound_permissions[0].property_value, '0.0.0.0/0')
        self.assertFalse(security_group.outbound_permissions[0].has_description)
        self.assertTrue(security_group.tags)

    @skip('CR-3092')
    @context(module_path="default-sg-with-rules")
    def test_default_sg_with_rules(self, ctx: AwsEnvironmentContext):
        security_group = next((sg for sg in ctx.security_groups
                               if sg.name == 'examplerulename'), None)
        self.assertIsNotNone(security_group)
        self.assertTrue(security_group.has_description)
        self.assertEqual(len(security_group.inbound_permissions), 1)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(security_group.inbound_permissions[0].from_port, 0)
        self.assertEqual(security_group.inbound_permissions[0].to_port, 65535)
        self.assertEqual(security_group.inbound_permissions[0].property_value, security_group.security_group_id)
        self.assertEqual(security_group.inbound_permissions[0].property_type, SecurityGroupRulePropertyType.SECURITY_GROUP_ID)
        self.assertFalse(security_group.inbound_permissions[0].has_description)
        self.assertEqual(security_group.outbound_permissions[0].from_port, 0)
        self.assertEqual(security_group.outbound_permissions[0].to_port, 65535)
        self.assertEqual(security_group.outbound_permissions[0].property_value, security_group.security_group_id)
        self.assertEqual(security_group.outbound_permissions[0].property_type, SecurityGroupRulePropertyType.SECURITY_GROUP_ID)
        self.assertFalse(security_group.outbound_permissions[0].has_description)
        self.assertTrue(security_group.tags)
