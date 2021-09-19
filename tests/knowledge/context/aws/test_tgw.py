from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestTgw(AwsContextTest):

    def get_component(self):
        return "tgw"

    @context(module_path="tgw_with_routes_and_tags")
    def test_tgw_with_routes_and_tags(self, ctx: AwsEnvironmentContext):
        for tgw in ctx.transit_gateways:
            self.assertTrue(tgw.tags)
        tgw = next((tgw for tgw in ctx.transit_gateways if tgw.name == 'tgw-046489dd079b37629'), None)
        if tgw:
            self.assertEqual(tgw.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/directconnect/v2/home?region=us-east-1#'
                             '/transit-gateways/arn:aws:ec2:us-east-1:100552308875:tgw-046489dd079b37629')

        tgw_attach = next((tgw_attach for tgw_attach in ctx.transit_gateway_attachments if tgw_attach.tags), None)
        self.assertIsNotNone(tgw_attach)
        for tgw_rt in ctx.transit_gateway_route_tables:
            self.assertTrue(tgw_rt.tags)
