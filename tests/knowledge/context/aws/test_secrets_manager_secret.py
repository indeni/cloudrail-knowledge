from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSecretsManagerSecret(AwsContextTest):

    def get_component(self):
        return "secrets_manager"

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        secret = next((secret for secret in ctx.secrets_manager_secrets if secret.sm_name == 'not_secure_secret'), None)
        self.assertIsNotNone(secret)
        self.assertTrue(secret.arn)
        self.assertFalse(secret.tags)
        self.assertEqual(secret.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/secretsmanager/home?region=us-east-1#!/secret?name=not_secure_secret')

    @context(module_path="secure_policy")
    def test_secure_policy_policy_var(self, ctx: AwsEnvironmentContext):
        if ctx.secrets_manager_secrets_policies:
            secret_policy = next((secret_policy for secret_policy in ctx.secrets_manager_secrets_policies
                                  if secret_policy.statements[0].actions ==
                                  ["secretsmanager:GetSecretValue", "secretsmanager:ListSecrets"]
                                  and secret_policy.statements[0].effect == StatementEffect.ALLOW), None)
            self.assertIsNotNone(secret_policy)
            self.assertTrue(secret_policy.secret_arn)

    @context(module_path="secure_policy")
    def test_secure_policy(self, ctx: AwsEnvironmentContext):
        secret = next((secret for secret in ctx.secrets_manager_secrets if secret.sm_name == 'secure_secret_1'), None)
        self.assertIsNotNone(secret)
        self.assertTrue(secret.arn)
        self.assertEqual(secret.policy.statements[0].actions, ["secretsmanager:GetSecretValue", "secretsmanager:ListSecrets"])
        self.assertEqual(secret.policy.statements[0].effect, StatementEffect.ALLOW)

    @context(module_path="encrypted_at_rest_with_aws_managed_key", base_scanner_data_for_iac='account-data-ssm-param-kms-keys',
             test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_at_rest_with_aws_managed_key(self, ctx: AwsEnvironmentContext):
        secret = next((secret for secret in ctx.secrets_manager_secrets if secret.sm_name == 'test-cloudrail-1'), None)
        self.assertIsNotNone(secret)
        self.assertTrue(secret.arn)
        self.assertEqual(secret.kms_key, 'arn:aws:kms:us-east-1:115553109071:key/3b06df86-fde7-49cd-adbb-0a4c008d3df0')
        self.assertNotEqual(secret.kms_data.key_manager.value, 'CUSTOMER')
        self.assertNotEqual(secret.kms_data.key_manager.name, 'CUSTOMER')

    @context(module_path="encrypted_at_rest_with_customer_managed_key", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_at_rest_with_customer_managed_key(self, ctx: AwsEnvironmentContext):
        secret = next((secret for secret in ctx.secrets_manager_secrets if secret.sm_name == 'test-cloudrail-2'), None)
        self.assertIsNotNone(secret)
        self.assertTrue(secret.arn)
        self.assertTrue(secret.kms_key)
        self.assertEqual(secret.kms_data.key_manager.value, 'CUSTOMER')
        self.assertEqual(secret.kms_data.key_manager.name, 'CUSTOMER')

    @context(module_path="not_secure_policy_with_tags")
    def test_not_secure_policy_with_tags(self, ctx: AwsEnvironmentContext):
        secret = next((secret for secret in ctx.secrets_manager_secrets if secret.sm_name == 'not_secure_secret'), None)
        self.assertIsNotNone(secret)
        self.assertTrue(secret.tags)
