from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestApiGatewayV2VpcLink(AwsContextTest):

    def get_component(self):
        return "api_gateway_v2"

    @context(module_path="with_vpc_link")
    def test_with_vpc_link(self, ctx: AwsEnvironmentContext):
        vpc_link = next((vpc_link for vpc_link in ctx.api_gateway_v2_vpc_links
                         if vpc_link.name == 'mrw-link'), None)
        self.assertIsNotNone(vpc_link)
        self.assertTrue(vpc_link.vpc_link_id)
        self.assertTrue(vpc_link.get_arn())
        self.assertTrue(vpc_link.security_group_ids)
        self.assertTrue(vpc_link.subnet_ids)
        if not vpc_link.is_managed_by_iac:
            self.assertEqual(vpc_link.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/apigateway/main/vpc-links/list?region=us-east-1&vpcLink=xeuv2c')
