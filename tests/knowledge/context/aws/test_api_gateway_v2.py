from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestApiGateway(AwsContextTest):

    def get_component(self):
        return "api_gateway_v2"

    @context(module_path="with_vpc_link")
    def test_with_vpc_link(self, ctx: AwsEnvironmentContext):
        api_gw = next((api_gw for api_gw in ctx.api_gateways_v2 if api_gw.api_gw_name == 'mrw-http-api'), None)
        self.assertTrue(api_gw)
        self.assertEqual(api_gw.protocol_type, 'HTTP')
        self.assertTrue(api_gw.api_gw_id)
        self.assertTrue(api_gw.arn)
        if not api_gw.is_managed_by_iac:
            self.assertEqual(api_gw.get_arn(), 'arn:aws:apigateway:us-east-1::/apis/c24d67urkj')
            self.assertEqual(api_gw.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/apigateway/main/api-detail/?api=c24d67urkj&region=us-east-1')
        self.assertIsNotNone(api_gw.api_gw_integration)
        self.assertIsNotNone(api_gw.vpc_link)
        self.assertTrue(api_gw.get_all_network_configurations())
        self.assertTrue(len(api_gw.network_resource.network_interfaces) > 0)
