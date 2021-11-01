from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestXrayEncryption(AwsContextTest):

    def get_component(self):
        return 'xray'

    @context(module_path="kms_key_arn_aws_managed", base_scanner_data_for_iac='account-data-xray-kms-key-arn-aws-managed.zip',
             test_options=TestOptions(tf_version='>v3.4.0'))
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        xray = next((xray for xray in ctx.xray_encryption_configurations 
                     if xray.key_id == 'arn:aws:kms:us-east-1:115553109071:key/78026359-3e90-4538-a3d1-33f4fa4f102a'), None)
        self.assertTrue(xray.key_id)
        self.assertEqual(xray.kms_data.key_manager, KeyManager.AWS)
        self.assertEqual(xray.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/xray/home?region=us-east-1#/encryption-configuration')

    @context(module_path="kms_key_customer_creating", test_options=TestOptions(tf_version='>v3.4.0'))
    def test_kms_key_customer_creating(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.xray_encryption_configurations), 1)
        xray = ctx.xray_encryption_configurations[0]
        self.assertTrue(xray.key_id)
        self.assertEqual(xray.kms_data.key_manager, KeyManager.CUSTOMER)

    @context(module_path="no_kms_encryption", test_options=TestOptions(tf_version='>v3.4.0'))
    def test_no_kms_encryption(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.xray_encryption_configurations), 1)
        xray = ctx.xray_encryption_configurations[0]
        self.assertFalse(xray.key_id)
        self.assertIsNone(xray.kms_data)

    @context(module_path="kms_key_customer_existing", base_scanner_data_for_iac='account-data-xray-kms-key-customer-existing.zip',
             test_options=TestOptions(tf_version='>v3.4.0'))
    def test_kms_key_customer_existing(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.xray_encryption_configurations), 1)
        xray = ctx.xray_encryption_configurations[0]
        self.assertTrue(xray.key_id)
        self.assertEqual(xray.kms_data.key_manager, KeyManager.CUSTOMER)
