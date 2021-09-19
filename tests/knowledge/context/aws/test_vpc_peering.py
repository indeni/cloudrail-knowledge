import unittest

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class TestVpcPeering(AwsContextTest):

    def get_component(self):
        return 'vpc_peering'

    @context(module_path="peering_with_chkp_fw")
    def test_peering_with_chkp_fw(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.peering_connections), 1)
        peering_routes = [route for route in ctx.routes if route.peering_connection]
        self.assertEqual(len(peering_routes), 3)
        self.assertTrue(
            all(
                any(route.destination == destination for route in peering_routes)
                for destination in ['10.50.1.0/24', '10.60.10.0/24', '10.60.20.0/24']
            )
        )

    @unittest.skip('Depends on CR-592')
    @context(module_path="simple_case_within_one_account")
    def test_simple_case_within_one_account(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.peering_connections), 1)
        peering_routes = [route for route in ctx.routes if route.peering_connection]
        self.assertEqual(len(peering_routes), 1)
        self.assertTrue(peering_routes[0].destination == '0.0.0.0/0')

    @context(module_path="peering_with_chkp_fw", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_peering_with_chkp_fw_testing_url(self, ctx: AwsEnvironmentContext):
        peering = next((peering for peering in ctx.peering_connections if peering.peering_id == 'pcx-08b0015769041f20e'), None)
        self.assertIsNotNone(peering)
        self.assertEqual(peering.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/vpc/home?region=us-east-1#'
                         'PeeringConnections:vpcPeeringConnectionId=pcx-08b0015769041f20e')
