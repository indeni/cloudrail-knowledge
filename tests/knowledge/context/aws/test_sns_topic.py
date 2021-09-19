from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestSnsTopic(AwsContextTest):

    def get_component(self):
        return "sns_topics"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sns_topics), 1)
        for sns_topic in ctx.sns_topics:
            self.assertTrue(sns_topic.encrypted_at_rest)
            self.assertTrue(sns_topic.sns_arn)
            self.assertEqual(sns_topic.sns_name, 'sns_ecnrypted')
            if not sns_topic.is_new_resource():
                self.assertEqual(sns_topic.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/sns/v3/home?region=us-east-1#'
                                 '/topic/arn:aws:sns:us-east-1:115553109071:sns_ecnrypted')

    @context(module_path="encrypted_at_rest_with_aws_managed_key_by_key_arn",
             base_scanner_data_for_iac='account-data-existsing-keys-xray/kms_key_arn_aws_managed', test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_at_rest_with_aws_managed_key_by_key_arn(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sns_topics), 1)
        for sns_topic in ctx.sns_topics:
            self.assertTrue(sns_topic.encrypted_at_rest)
            self.assertTrue(sns_topic.sns_arn)
            self.assertEqual(sns_topic.sns_name, 'sns_ecnrypted')
            self.assertTrue(sns_topic.kms_data.arn)
            self.assertTrue(isinstance(sns_topic.kms_data.key_manager, KeyManager))
            if not sns_topic.is_new_resource():
                self.assertEqual(sns_topic.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/sns/v3/home?region=us-east-1#'
                                 '/topic/arn:aws:sns:us-east-1:115553109071:sns_ecnrypted')

    @context(module_path="encrypted_at_rest_with_customer_managed_key_creating_key")
    def test_encrypted_at_rest_with_customer_managed_key_creating_key(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sns_topics), 1)
        for sns_topic in ctx.sns_topics:
            self.assertTrue(sns_topic.encrypted_at_rest)
            self.assertTrue(sns_topic.sns_arn)
            self.assertEqual(sns_topic.sns_name, 'sns_ecnrypted')
            self.assertTrue(sns_topic.kms_data.arn)
            self.assertTrue(isinstance(sns_topic.kms_data.key_manager, KeyManager))
            if not sns_topic.is_new_resource():
                self.assertEqual(sns_topic.get_cloud_resource_url(),
                                 'https://console.aws.amazon.com/sns/v3/home?region=us-east-1#'
                                 '/topic/arn:aws:sns:us-east-1:115553109071:sns_ecnrypted')

    @context(module_path="not_encrypted_at_rest_2_units")
    def test_not_encrypted_at_rest_2_units(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sns_topics), 2)
        for sns_topic in ctx.sns_topics:
            self.assertFalse(sns_topic.encrypted_at_rest)
            self.assertTrue(sns_topic.sns_arn)
            self.assertTrue('sns_not_ecnrypted' in sns_topic.sns_name)
            self.assertFalse(sns_topic.tags)

    @context(module_path="not_encrypted_with_tags")
    def test_not_encrypted_with_tags(self, ctx: AwsEnvironmentContext):
        sns_topic = next((sns for sns in ctx.sns_topics if sns.sns_name == 'sns_not_ecnrypted-1'), None)
        self.assertIsNotNone(sns_topic)
        self.assertTrue(sns_topic.tags)
