from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestKmsAlias(AwsContextTest):

    def get_component(self):
        return "kms_aliases"

    @context(module_path="basic")
    def test_basic(self, ctx: AwsEnvironmentContext):
        alias = next((alias for alias in ctx.kms_aliases
                      if alias.alias_name == 'alias/cloudrail-alias'), None)
        self.assertIsNotNone(alias)
        self.assertTrue(alias.alias_arn)
        self.assertTrue(alias.target_key_id)
        self.assertEqual(alias.key_manager, KeyManager.CUSTOMER)
        if not alias.is_managed_by_iac:
            self.assertEqual(alias.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/kms/home?region=us-east-1#/kms/keys/82fbafc1-4689-4cf6-acee-8309fbcb3985')

    @context(module_path="basic", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_for_aws_url(self, ctx: AwsEnvironmentContext):
        aws_alias = next((alias for alias in ctx.kms_aliases
                          if alias.alias_name == 'alias/aws/backup'), None)
        self.assertEqual(aws_alias.key_manager, KeyManager.AWS)
        if not aws_alias.is_managed_by_iac:
            self.assertEqual(aws_alias.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/kms/home?region=us-east-1#/kms/defaultKeys/3711dac5-587c-4a45-9d48-dfcfbdc3586b')
