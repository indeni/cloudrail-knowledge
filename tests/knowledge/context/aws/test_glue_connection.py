from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestGlueConnection(AwsContextTest):

    def get_component(self):
        return "glue_connections"

    @context(module_path="basic_networking", test_options=TestOptions(run_cloudmapper=False))
    def test_basic_networking(self, ctx: AwsEnvironmentContext):
        connection = next((connection for connection in ctx.glue_connections if connection.connection_name == 'test_glue_connection'), None)
        self.assertIsNotNone(connection)
        self.assertTrue(connection.arn)
        self.assertFalse(connection.vpc_config.assign_public_ip)
        self.assertTrue(connection.vpc_config.subnet_list_ids)
        self.assertTrue(connection.vpc_config.security_groups_ids)
        self.assertEqual(connection.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/glue/home?region=us-east-1#connection:name=test_glue_connection')
        self.assertTrue(len(connection.network_resource.network_interfaces) > 0)

    @context(module_path="networking_no_sg", test_options=TestOptions(run_cloudmapper=False))
    def test_networking_no_sg(self, ctx: AwsEnvironmentContext):
        connection = next((connection for connection in ctx.glue_connections if connection.connection_name == 'test_glue_connection'), None)
        self.assertIsNotNone(connection)
        self.assertTrue(connection.arn)
        self.assertFalse(connection.vpc_config.assign_public_ip)
        self.assertTrue(connection.vpc_config.subnet_list_ids)
        self.assertFalse(connection.vpc_config.security_groups_ids)
        self.assertTrue(len(connection.network_resource.network_interfaces) == 0)
