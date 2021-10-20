from typing import List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import LaunchConfiguration
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import AssociatePublicIpAddress
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.connection import ConnectionDirectionType, PolicyConnectionProperty, PolicyEvaluation, PrivateConnectionDetail
from cloudrail.knowledge.utils.policy_evaluator import is_any_action_allowed

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestEc2(AwsContextTest):

    def get_component(self):
        return "ec2"

    @context(module_path="checkpoint_fw_cluster")
    def test_checkpoint_fw_cluster(self, ctx: AwsEnvironmentContext):
        self._vpc_assertion(ctx, False, ["10.0.0.0/16"], "my-vpc")
        launch_config: LaunchConfiguration = ctx.launch_configurations[0]
        self.assertIsNotNone(launch_config.image_id)
        security_group = next((security_group for security_group in ctx.security_groups
                               if security_group.name == 'permissive_security_group'), None)
        self.assertEqual(security_group.security_group_id, launch_config.security_group_ids[0])

        autoscaling_grp = ctx.auto_scaling_groups[0]
        self.assertIsNotNone(autoscaling_grp.name)
        self.assertIs(launch_config, autoscaling_grp.launch_configuration)
        self.assertEqual(len(ctx.ec2s), 3)
        for subnet_id in autoscaling_grp.subnet_ids:
            self.assertTrue(any(ec2.network_resource.subnet_ids == [subnet_id] for ec2 in ctx.ec2s))

    @context(module_path="defaults_only")
    def test_defaults_only(self, ctx: AwsEnvironmentContext):
        ec2instance = ctx.ec2s[0]
        self.assertTrue(ec2instance.network_resource.subnets[0].is_default)
        self.assertTrue(next(iter(ec2instance.network_resource.security_groups)).is_default)
        ec2instance = next(ec2 for ec2 in ctx.ec2s if ec2.name == 'my_ec2')
        if ec2instance.raw_data.associate_public_ip_address:
            self.assertEqual(AssociatePublicIpAddress.USE_SUBNET_SETTINGS, ec2instance.raw_data.associate_public_ip_address)
        self.assertTrue(ec2instance.network_resource.subnets[0].is_default)
        self.assertTrue(next(iter(ec2instance.network_resource.security_groups)).is_default)
        self.assertIsNotNone(ec2instance.account)
        self.assertEqual(ec2instance.http_tokens, 'optional')
        self.assertTrue(ec2instance.tags)
        self.assertEqual(ec2instance.instance_type, 't2.micro')
        self.assertFalse(ec2instance.ebs_optimized)
        if not ec2instance.is_managed_by_iac:
            self.assertEqual(ec2instance.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#InstanceDetails:instanceId=i-03e54d61c76b6b694')

    @context(module_path="in_subnet")
    def test_in_subnet(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, ["10.0.0.0/16"], "my-vpc")
        subnet = next(subnet for subnet in ctx.subnets if subnet.vpc == vpc and subnet.cidr_block == '10.0.1.0/24')
        ec2instance = ctx.ec2s[0]
        self.assertTrue(subnet.subnet_id in ec2instance.network_resource.subnet_ids)
        self.assertEqual(vpc.default_security_group.security_group_id, next(iter(ec2instance.network_resource.security_groups)).security_group_id)
        self.assertTrue(len(ec2instance.network_resource.outbound_connections) > 0)
        egress_to_internet = ec2instance.network_resource.outbound_connections[0]
        self.assertEqual(ConnectionDirectionType.OUTBOUND, egress_to_internet.connection_direction_type)
        self.assertEqual(egress_to_internet.connection_property.ports[0], (0, 65535))
        self.assertIsNotNone(ec2instance.account)
        self.assertEqual('my_ec2', ec2instance.tags['Name'])

    @context(module_path="using_common_module")
    def test_using_common_module(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, ["10.0.0.0/16"], "my-vpc")
        subnet = next(subnet for subnet in ctx.subnets if subnet.vpc == vpc and subnet.cidr_block == "10.0.1.0/24")
        ec2s = [ec2 for ec2 in ctx.ec2s if ec2.network_resource.vpc == vpc]
        self.assertEqual(2, len(ec2s))

        self.assertEqual(2, len(ctx.ec2s))
        ec2_1 = ctx.ec2s[0]
        ec2_2 = ctx.ec2s[1]

        self.assertTrue(subnet.subnet_id in ec2_1.network_resource.subnet_ids)
        self.assertTrue(subnet.subnet_id in ec2_2.network_resource.subnet_ids)

        self.assertIsNone(ec2_1.raw_data.public_ip_address)
        self.assertIsNone(ec2_1.raw_data.public_ip_address)

        self.assertTrue(len(ec2_1.network_resource.public_ip_addresses) == 0)
        self.assertTrue(len(ec2_2.network_resource.public_ip_addresses) == 0)

        self.assertFalse(ec2_1.network_resource.is_inbound_public)
        self.assertFalse(ec2_2.network_resource.is_inbound_public)

        self.assertIsNotNone(ec2_1.account)
        self.assertIsNotNone(ec2_2.account)

    @context(module_path="conflict_between_subnet_and_ec2_public_settings")
    def test_conflict_between_subnet_and_ec2_public_settings(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, ["10.0.0.0/16"], "my-vpc")
        subnet = next(subnet for subnet in ctx.subnets if subnet.vpc == vpc and subnet.cidr_block == "10.0.0.0/24")

        self.assertEqual(1, len(ctx.ec2s))
        ec2_1 = ctx.ec2s[0]

        self.assertTrue(subnet.map_public_ip_on_launch)

        # If the EC2 specific asks NOT to have a public IP address, it won't have one,
        # even if the subnet says it should
        self.assertEqual(0, len(ec2_1.network_resource.public_ip_addresses))

    @context(module_path="http_tokens_required")
    def test_http_tokens_required(self, ctx: AwsEnvironmentContext):
        ec2instance = ctx.ec2s[0]
        self.assertEqual(ec2instance.http_tokens, 'required')

    @context(module_path="using_gitlab_runner_module")
    def test_using_gitlab_runner_module(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 1)
        ec2 = ctx.ec2s[0]
        self.assertTrue(ec2.iam_role)
        self.assertEqual(ec2.iam_role.role_name, 'spot-runners-instance-role')
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertEqual(len(ec2.network_resource.security_groups), 1)
        self.assertFalse(next(iter(ec2.network_resource.security_groups)).is_default)
        asg = ctx.auto_scaling_groups[0]
        self.assertEqual(len(asg.subnet_ids), 1)
        self.assertTrue(asg.launch_configuration)
        self.assertIsNone(asg.launch_template)
        self.assertEqual(len(asg.launch_configuration.security_group_ids), 1)
        self.assertTrue(asg.subnet_ids[0] in ec2.network_resource.subnets[0].aliases)
        self.assertTrue(asg.launch_configuration.security_group_ids[0] in next(iter(ec2.network_resource.security_groups)).aliases)

    @context(module_path='using_cloud42_bastion_module')
    def test_using_cloud42_bastion_module(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.ec2s), 1)
        ec2 = ctx.ec2s[0]
        self.assertTrue(ec2.iam_role)
        self.assertEqual(ec2.iam_role.role_name, 'prod_bastion_role')
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertEqual(len(ec2.network_resource.security_groups), 1)
        self.assertTrue(next(iter(ec2.network_resource.security_groups)).is_default)
        asg = ctx.auto_scaling_groups[0]
        self.assertEqual(len(asg.subnet_ids), 1)
        self.assertTrue(asg.launch_configuration)
        self.assertIsNone(asg.launch_template)
        self.assertEqual(len(asg.launch_configuration.security_group_ids), 1)
        self.assertTrue(asg.subnet_ids[0] in ec2.network_resource.subnets[0].aliases)
        self.assertTrue(asg.launch_configuration.security_group_ids[0] in next(iter(ec2.network_resource.security_groups)).aliases)

    def _vpc_assertion(self, ctx: AwsEnvironmentContext, default_vpc: bool, cidr_block: List[str], vpc_name: str) -> Vpc:
        vpc: Vpc = next((vpc for vpc in ctx.vpcs if vpc.name == vpc_name), None)
        self.assertEqual(cidr_block, vpc.cidr_block)
        self.assertEqual(vpc_name, vpc.name)
        self.assertEqual("us-east-1", vpc.region)
        self.assertIsNotNone(vpc.account)
        self.assertEqual(default_vpc, vpc.is_default)
        self.assertIsNotNone(vpc.main_route_table)
        return vpc

    @context(module_path="ec2_private_images_only")
    def test_ec2_private_images_only(self, ctx: AwsEnvironmentContext):
        for ec2 in ctx.ec2s:
            self.assertFalse(ec2.image_data.is_public)

    @context(module_path="ec2_3private_1public_image")
    def test_ec2_3private_1public_image(self, ctx: AwsEnvironmentContext):
        self.assertTrue(any(ec2.image_data.is_public for ec2 in ctx.ec2s))

    # Not running drift as were unable to create drift data.
    @context(module_path="ec2-outbound-permissions-connections", test_options=TestOptions(run_drift_detection=False))
    def test_ec2_outbound_permissions_connections(self, ctx: AwsEnvironmentContext):
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'ec2-web-server'), None)
        bucket = ctx.s3_buckets.get('atotalyrandomname929293')
        self.assertIsNotNone(ec2)
        self.assertIsNotNone(bucket)

        conn = next((connection for connection in ec2.outbound_connections
                     if isinstance(connection, PrivateConnectionDetail) and connection.target_instance == bucket), None)
        self.assertIsNotNone(conn)

        policy_conn: PolicyConnectionProperty = conn.connection_property
        self.assertEqual(len(policy_conn.policy_evaluation), 1)
        policy_eval: PolicyEvaluation = policy_conn.policy_evaluation[0]
        self.assertTrue(is_any_action_allowed(policy_eval))

    @context(module_path="no_tags")
    def test_no_tags(self, ctx: AwsEnvironmentContext):
        for ec2 in ctx.ec2s:
            self.assertFalse(ec2.tags)

    @context(module_path="monitoring_enabled")
    def test_monitoring_enabled(self, ctx: AwsEnvironmentContext):
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'test-monitoring'), None)
        self.assertIsNotNone(ec2)
        self.assertTrue(ec2.monitoring_enabled)

    @context(module_path="monitoring_disabled")
    def test_monitoring_disabled(self, ctx: AwsEnvironmentContext):
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'test-monitoring'), None)
        self.assertIsNotNone(ec2)
        self.assertFalse(ec2.monitoring_enabled)
