from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestGlacierVault(AwsContextTest):

    def get_component(self):
        return "glacier_vault"

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.glacier_vaults), 1)
        for gc_vault in ctx.glacier_vaults:
            self.assertTrue(gc_vault.arn)
            self.assertEqual(gc_vault.vault_name, 'not_secure_archive')
            self.assertFalse(gc_vault.tags)
            self.assertEqual(gc_vault.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/glacier/home?region=us-east-1#/vaults')

    @context(module_path="not_secure_policy")
    def test_not_secure_policy_poloicy_var(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.glacier_vaults_policies), 1)
        for gc_vault_policy in ctx.glacier_vaults_policies:
            self.assertTrue(gc_vault_policy.vault_arn)
            self.assertEqual(gc_vault_policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(gc_vault_policy.statements[0].actions, ['glacier:*'])

    @context(module_path="with_tags")
    def test_not_secure_policy_with_tags(self, ctx: AwsEnvironmentContext):
        vault = next((vault for vault in ctx.glacier_vaults if vault.vault_name == 'not_secure_archive'), None)
        self.assertIsNotNone(vault)
        self.assertTrue(vault.tags)
