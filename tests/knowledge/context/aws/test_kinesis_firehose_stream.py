from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestKinesisFirehoseStream(AwsContextTest):

    def get_component(self):
        return "kinesis_firehose_streams"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.kinesis_firehose_streams), 1)
        firehose = next((firehose for firehose in ctx.kinesis_firehose_streams
                         if firehose.stream_name == 'cloudrail-firehose-test-encrypted'), None)
        self.assertIsNotNone(firehose)
        self.assertTrue(firehose.stream_arn)
        self.assertTrue(firehose.encrypted_at_rest)
        self.assertEqual(firehose.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/firehose/home?region=us-east-1#/details/cloudrail-firehose-test-encrypted')

    @context(module_path="not_encrypted")
    def test_not_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.kinesis_firehose_streams), 1)
        firehose = next((firehose for firehose in ctx.kinesis_firehose_streams
                         if firehose.stream_name == 'cloudrail-firehose-test-non-encrypted'), None)
        self.assertIsNotNone(firehose)
        self.assertTrue(firehose.stream_arn)
        self.assertFalse(firehose.encrypted_at_rest)
        self.assertFalse(firehose.tags)

    @context(module_path="with_tags")
    def test_not_encrypted_with_tags(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.kinesis_firehose_streams), 1)
        firehose = next((firehose for firehose in ctx.kinesis_firehose_streams
                         if firehose.stream_name == 'cloudrail-firehose-test-non-encrypted'), None)
        self.assertIsNotNone(firehose)
        self.assertTrue(firehose.tags)

    @context(module_path="kinesis_networking_to_es", test_options=TestOptions(tf_version='>v3.5.0'))
    def test_kinesis_networking_to_es(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.kinesis_firehose_streams), 1)
        firehose = next((firehose for firehose in ctx.kinesis_firehose_streams
                         if firehose.stream_name == 'terraform-kinesis-firehose-es'), None)
        self.assertIsNotNone(firehose)
        self.assertTrue(firehose.es_domain_arn)
        self.assertTrue(firehose.get_all_network_configurations())
