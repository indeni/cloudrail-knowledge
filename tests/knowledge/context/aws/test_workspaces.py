from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestWorkspaces(AwsContextTest):

    def get_component(self):
        return 'workspaces/workspaces'

    @context(module_path="root_volume_encrypted_at_rest")
    def test_root_volume_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = next((workspace for workspace in ctx.workspaces
                          if workspace.volume_encryption_key), None)
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertTrue(workspace.volume_encryption_key)
        if not workspace.is_managed_by_iac:
            self.assertEqual(workspace.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/workspaces/home?region=us-east-1#listworkspaces:search=ws-xf7fv8tby')

    @context(module_path="root_volume_not_encrypted_at_rest")
    def test_root_volume_not_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = next((workspace for workspace in ctx.workspaces
                          if not workspace.volume_encryption_key), None)
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertFalse(workspace.volume_encryption_key)
        self.assertFalse(workspace.tags)

    @context(module_path="user_volume_encrypted_at_rest")
    def test_user_volume_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = next((workspace for workspace in ctx.workspaces
                          if workspace.volume_encryption_key), None)
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertTrue(workspace.volume_encryption_key)

    @context(module_path="user_volume_not_encrypted_at_rest")
    def test_user_volume_not_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = next((workspace for workspace in ctx.workspaces
                          if not workspace.volume_encryption_key), None)
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertFalse(workspace.volume_encryption_key)

    @context(module_path="user_volume_encrypted_with_aws_managed_cmk")
    def test_user_volume_encrypted_with_aws_managed_cmk(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = ctx.workspaces[0]
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertTrue(workspace.volume_encryption_key)
        self.assertTrue(workspace.user_encryption_enabled)

    @context(module_path="user_volume_encrypted_with_customer_managed_cmk_creating_key")
    def test_user_volume_encrypted_with_customer_managed_cmk_creating_key(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = ctx.workspaces[0]
        self.assertIsNotNone(workspace)
        self.assertTrue(workspace.workspace_id)
        self.assertTrue(workspace.volume_encryption_key)
        self.assertTrue(workspace.user_encryption_enabled)

    @context(module_path="with_tags")
    def test_root_volume_not_encrypted_at_rest_with_tags(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.workspaces), 1)
        workspace = next((workspace for workspace in ctx.workspaces
                          if not workspace.volume_encryption_key), None)
        self.assertTrue(workspace.tags)
