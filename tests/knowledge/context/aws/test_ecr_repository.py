from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestEcrRepository(AwsContextTest):

    def get_component(self):
        return "ecr_repositories"

    @context(module_path="non_secure_policy")
    def test_non_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.ecr_repositories), 1)
        ecr_repo = ctx.ecr_repositories[0]
        self.assertTrue(ecr_repo.arn)
        self.assertFalse(ecr_repo.tags)
        self.assertEqual(ecr_repo.repo_name, 'not_secure_ecr')
        self.assertEqual(ecr_repo.policy.statements[0].actions, ['ecr:*'])
        self.assertEqual(ecr_repo.policy.statements[0].effect, StatementEffect.ALLOW)
        if not ecr_repo.is_managed_by_iac:
            self.assertEqual(ecr_repo.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ecr/repositories/private/115553109071/not_secure_ecr?region=us-east-1')

    @context(module_path="secure_policy")
    def test_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.ecr_repositories), 1)
        ecr_repo = ctx.ecr_repositories[0]
        self.assertTrue(ecr_repo.arn)
        self.assertEqual(ecr_repo.repo_name, 'secure_ecr')
        self.assertTrue(any(['ecr:*'] != action for action in ecr_repo.policy.statements[0].actions))

    @context(module_path="with_tags")
    def test_non_secure_policy_with_tags(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'not_secure_ecr'), None)
        self.assertIsNotNone(ecr)
        self.assertTrue(ecr.tags)
        self.assertEqual(ecr.image_tag_mutability, 'MUTABLE')

    @context(module_path="image_tag_immutable")
    def test_image_tag_immutable(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'cloudrail-test-immutable'), None)
        self.assertIsNotNone(ecr)
        self.assertEqual(ecr.image_tag_mutability, 'IMMUTABLE')

    @context(module_path="default_encryption", test_options=TestOptions(tf_version='>3.1.0'))
    def test_default_encryption(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(ecr)
        self.assertEqual(ecr.encryption_type, 'AES256')
        self.assertFalse(ecr.kms_key_id)
        self.assertFalse(ecr.kms_data)

    @context(module_path="encrypted_cmk_new_key", test_options=TestOptions(tf_version='>3.1.0'))
    def test_encrypted_cmk_new_key(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(ecr)
        self.assertEqual(ecr.encryption_type, 'KMS')
        self.assertTrue(ecr.kms_key_id)
        self.assertEqual(ecr.kms_data.key_manager, KeyManager.CUSTOMER)

    @context(module_path="encrypted_using_aws_key", base_scanner_data_for_iac='account-data-ecr-repo-kms-keys', test_options=TestOptions(tf_version='>3.1.0'))
    def test_encrypted_using_aws_key(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(ecr)
        self.assertEqual(ecr.encryption_type, 'KMS')
        self.assertTrue(ecr.kms_key_id)
        self.assertEqual(ecr.kms_data.key_manager, KeyManager.AWS)
        self.assertFalse(ecr.is_image_scan_on_push)

    @context(module_path="image_scan_push_enabled")
    def test_image_scan_push_enabled(self, ctx: AwsEnvironmentContext):
        ecr = next((ecr for ecr in ctx.ecr_repositories if ecr.repo_name == 'cloudrail-test-on-push-enabled'), None)
        self.assertIsNotNone(ecr)
        self.assertTrue(ecr.is_image_scan_on_push)
