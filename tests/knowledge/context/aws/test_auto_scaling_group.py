from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import AutoScalingGroup
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAutoScalingGroup(AwsContextTest):

    def get_component(self):
        return "auto_scaling_group"

    @context(module_path="launch-template")
    def test_launch_template(self, ctx: AwsEnvironmentContext):
        asg: AutoScalingGroup = self._assert_asg(ctx)
        launch_temp: LaunchTemplate = asg.launch_template
        self.assertEqual(launch_temp.template_id, ctx.launch_templates[0].template_id)
        self.assertEqual(launch_temp.version_number, ctx.launch_templates[0].version_number)
        self.assertTrue((len(launch_temp.security_groups) == 0 and len(launch_temp.security_group_ids) == 0) or
                        (launch_temp.security_groups[0].security_group_id == launch_temp.security_group_ids[0]))
        self.assertEqual(ctx.ec2s[0].network_resource.public_ip_addresses, ['0.0.0.0'])

    @context(module_path="launch-template-default-settings")
    def test_launch_template_default_settings(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 2)
        for ec2 in ctx.ec2s:
            self.assertEqual(len(ec2.network_resource.subnets), 1)
            self.assertEqual(len(ec2.network_resource.public_ip_addresses) == 1, ec2.network_resource.subnets[0].map_public_ip_on_launch)
            self.assertEqual(len(ec2.network_resource.security_groups), 1)
            self.assertTrue(next(iter(ec2.network_resource.security_groups)).is_default)

    @context(module_path="launch-template-network-interfaces")
    def test_launch_template_network_interfaces(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 2)
        ec2: Ec2Instance = ctx.ec2s[0]
        self.assertEqual(len(ec2.network_resource.public_ip_addresses), 0)
        self.assertEqual(len(ec2.network_resource.subnets), 2)
        self.assertEqual(len(ec2.network_resource.security_groups), 2)

    @context(module_path="launch-template-network-interfaces-settings-only")
    def test_launch_template_network_interfaces_settings_only(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 1)
        ec2: Ec2Instance = ctx.ec2s[0]
        self.assertEqual(len(ec2.network_resource.public_ip_addresses), 0)
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertEqual(len(ec2.network_resource.security_groups), 1)

    @context(module_path="launch-configuration-settings-v1")
    def test_launch_configuration_settings(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 1)
        ec2: Ec2Instance = ctx.ec2s[0]
        self.assertEqual(len(ec2.network_resource.public_ip_addresses), 1)
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertEqual(len(ec2.network_resource.security_groups), 1)

    @context(module_path="launch-configuration-default-settings-v1")
    def test_launch_configuration_default_settings(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 1)
        ec2: Ec2Instance = ctx.ec2s[0]
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertEqual(len(ec2.network_resource.security_groups), 1)
        self.assertEqual(len(ec2.network_resource.public_ip_addresses), 1)

    def _assert_asg(self, ctx: AwsEnvironmentContext) -> AutoScalingGroup:
        self.assertGreater(len(ctx.auto_scaling_groups), 0)
        asg: AutoScalingGroup = ctx.auto_scaling_groups[0]
        self.assertEqual(asg.name, 'test-autoscaling-group')
        self.assertIsNotNone(ctx.subnets.get(asg.subnet_ids[0]))
        self.assertEqual(asg.region, 'us-east-1')
        self.assertEqual(asg.account, self.DUMMY_ACCOUNT_ID)

        if asg.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(asg.arn, 'aws_autoscaling_group.test-autoscaling-group.arn')
        elif asg.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(asg.arn, 'arn:aws:autoscaling:us-east-1:111111111111:autoScalingGroup:da425d3a-8726-4a36-bf1d-c5853fffa6e5:'
                                      'autoScalingGroupName/test-autoscaling-group')
            self.assertEqual(asg.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ec2autoscaling/home?region=us-east-1#/details/test-autoscaling-group?view=details')
        elif asg.origin == EntityOrigin.CLOUDFORMATION:
            self.assertEqual(asg.arn, 'arn:aws:autoscaling:us-east-1:111111111111:autoScalingGroup:d2ab4ece-8391-4473-891b-45570e5b3b41:autoScalingGroupName/test-autoscaling-group')
        return asg

    @context(module_path="launch-template-using-tag-field")
    def test_launch_template_using_tag_field(self, ctx: AwsEnvironmentContext):
        asg = next((asg for asg in ctx.auto_scaling_groups if asg.server_name == 'test-autoscaling-group'), None)
        self.assertIsNotNone(asg)
        self.assertTrue(all(tag_key in ('foo_hashcode', 'lorem_hashcode') for tag_key in asg.tags.keys()))
