from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestKmsKeys(AwsContextTest):

    def get_component(self):
        return "kms_keys"

    @context(module_path="kms_customer_managed")
    def test_kms_customer_managed(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.kms_keys), 1)
        for kms_key in ctx.kms_keys:
            self.assertEqual(kms_key.key_manager, KeyManager.CUSTOMER)
            self.assertTrue(kms_key.arn)
            self.assertTrue(kms_key.key_id)
            self.assertFalse(kms_key.tags)
            if not kms_key.is_managed_by_iac:
                self.assertEqual(kms_key.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/kms/home?region=us-east-1#/kms/keys/5bb6e506-13c9-45b5-a4fb-c10bad9ff4bc')

    @context(module_path="kms_aws_managed", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_kms_aws_managed(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.kms_keys), 6)
        for kms_key in ctx.kms_keys:
            self.assertEqual(kms_key.key_manager, KeyManager.AWS)
            self.assertTrue(kms_key.arn)
            self.assertTrue(kms_key.key_id)
        one_key = next((key for key in ctx.kms_keys if key.key_id == '33722bd4-8b1b-4564-92c9-549d0305149d'))
        self.assertEqual(one_key.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/kms/home?region=us-east-1#/kms/defaultKeys/33722bd4-8b1b-4564-92c9-549d0305149d')

    @context(module_path="aliases", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_aliases(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.kms_keys), 37)
        kms_key = next((kms_key for kms_key in ctx.kms_keys
                        if kms_key.alias_data and kms_key.alias_data.alias_name == 'alias/cloudrail-alias'), None)
        self.assertIsNotNone(kms_key)
        self.assertTrue(kms_key.alias_data.alias_arn)
        self.assertTrue(kms_key.alias_data.target_key_id)

    @context(module_path="kms_key_with_tags")
    def test_kms_key_with_tags(self, ctx: AwsEnvironmentContext):
        kms_key = next((kms_key for kms_key in ctx.kms_keys if kms_key.tags), None)
        self.assertIsNotNone(kms_key)
