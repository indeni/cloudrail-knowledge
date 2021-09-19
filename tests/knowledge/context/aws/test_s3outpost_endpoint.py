from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestS3OutpostEndpoint(AwsContextTest):

    def get_component(self):
        return "s3outpost_endpoint"

    @context(module_path="basic", test_options=TestOptions(run_cloudmapper=False, tf_version='>3.13.0'))
    def test_basic(self, ctx: AwsEnvironmentContext):
        endpoint = next((endpoint for endpoint in ctx.s3outpost_endpoints
                         if endpoint.outpost_id == 'op-0b6271f61a1b7f028'), None)
        self.assertIsNotNone(endpoint)
        self.assertTrue(endpoint.arn)
        self.assertTrue(endpoint.vpc_config.security_groups_ids)
        self.assertTrue(endpoint.vpc_config.subnet_list_ids)
        self.assertFalse(endpoint.vpc_config.assign_public_ip)
        self.assertEqual(endpoint.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/outposts/home?region=us-east-1#OutpostDetails:OutpostId=op-0b6271f61a1b7f028')
        self.assertTrue(len(endpoint.network_resource.network_interfaces) > 0)
