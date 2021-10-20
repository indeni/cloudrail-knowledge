from tests.knowledge.context.aws_context_test import AwsContextTest
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestWorkspaces(AwsContextTest):

    def get_component(self):
        return 'workspaces/workspaces_directories'

    @context(module_path="basic_networking")
    def test_basic_networking(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces_directories), 1)
        for directory in ctx.workspaces_directories:
            self.assertIsNotNone(directory)
            self.assertTrue(directory.directory_id)
            self.assertTrue(directory.subnet_ids)
            self.assertTrue(len(directory.subnet_ids), 2)
            self.assertTrue(directory.security_group_ids)
            self.assertTrue(len(directory.security_group_ids), 1)
            self.assertEqual(directory.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/workspaces/home?region=us-east-1#directories:directories')
            self.assertTrue(directory.get_all_network_configurations())
            self.assertTrue(directory.workspace_security_groups)
            self.assertTrue(directory.network_resource)

    @context(module_path="using_custom_security_group", test_options=TestOptions(tf_version='>3.11.0'))
    def test_using_custom_security_group(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces_directories), 1)
        for directory in ctx.workspaces_directories:
            self.assertIsNotNone(directory)
            self.assertTrue(directory.directory_id)
            self.assertTrue(directory.subnet_ids)
            self.assertTrue(len(directory.subnet_ids), 2)
            self.assertTrue(directory.security_group_ids)
            self.assertTrue(len(directory.security_group_ids), 2)
            self.assertTrue(directory.get_all_network_configurations())
            self.assertTrue(directory.workspace_security_groups)
            self.assertTrue(directory.network_resource)
