from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestWorkLinkFleet(AwsContextTest):

    def get_component(self):
        return 'worklink_fleet'

    @context(module_path="with_networking", test_options=TestOptions(run_cloudmapper=False))
    def test_with_networking(self, ctx: AwsEnvironmentContext):
        fleet = next((fleet for fleet in ctx.worklink_fleets if fleet.fleet_name == 'test'), None)
        self.assertIsNotNone(fleet)
        self.assertTrue(fleet.arn)
        self.assertFalse(fleet.vpc_config.assign_public_ip)
        self.assertTrue(fleet.vpc_config.subnet_list_ids)
        self.assertTrue(fleet.vpc_config.security_groups_ids)
        self.assertEqual(fleet.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/worklink/home?region=us-east-1#/fleets/details/test')
        self.assertTrue(len(fleet.network_resource.network_interfaces) > 0)

    @context(module_path="no_networking", test_options=TestOptions(run_cloudmapper=False))
    def test_no_networking(self, ctx: AwsEnvironmentContext):
        fleet = next((fleet for fleet in ctx.worklink_fleets if fleet.fleet_name == 'test-no-net'), None)
        self.assertIsNotNone(fleet)
        self.assertTrue(fleet.arn)
        self.assertFalse(fleet.get_all_network_configurations())
        self.assertTrue(len(fleet.network_resource.network_interfaces) == 0)
