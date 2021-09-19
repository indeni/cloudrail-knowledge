from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestEfs(AwsContextTest):

    def get_component(self):
        return "efs/efs_file_system"

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_file_systems), 1)
        for efs in ctx.efs_file_systems:
            self.assertTrue(efs.arn)
            self.assertEqual(efs.creation_token, 'efs-not-secure')
            self.assertTrue(efs.efs_id)
            self.assertFalse(efs.encrypted)

    @context(module_path="not_secure_policy")
    def test_not_secure_policy_policy_var(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_file_systems_policies), 1)
        for efs in ctx.efs_file_systems_policies:
            self.assertTrue(efs.efs_id)
            self.assertEqual(efs.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(efs.statements[0].actions, ['elasticfilesystem:*'])

    @context(module_path="efs_encrypted")
    def test_efs_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_file_systems), 1)
        for efs in ctx.efs_file_systems:
            self.assertTrue(efs.arn)
            self.assertEqual(efs.creation_token, 'cloudrail-encrypted')
            self.assertTrue(efs.efs_id)
            self.assertTrue(efs.encrypted)
            self.assertTrue(efs.tags)
            if not efs.is_managed_by_iac:
                self.assertEqual(efs.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/efs/home?region=us-east-1#/file-systems/fs-88cff67d')

    @context(module_path="no_tags")
    def test_efs_encrypted_no_tags(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.efs_file_systems), 1)
        for efs in ctx.efs_file_systems:
            self.assertFalse(efs.tags)
