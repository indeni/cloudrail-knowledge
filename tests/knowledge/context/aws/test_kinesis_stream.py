from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestKinesisStream(AwsContextTest):

    def get_component(self):
        return "kinesis_streams"

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.kinesis_streams), 1)
        kinesis_stream = next((kinesis_stream for kinesis_stream in ctx.kinesis_streams
                               if kinesis_stream.stream_name == 'cloudrail-test-encrypted'), None)
        self.assertIsNotNone(kinesis_stream)
        self.assertTrue(kinesis_stream.encrypted_at_rest)
        self.assertTrue(kinesis_stream.stream_arn)
        self.assertFalse(kinesis_stream.tags)
        self.assertEqual(kinesis_stream.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/kinesis/home?region=us-east-1#/streams/details/cloudrail-test-encrypted/details')

    @context(module_path="with_tags")
    def test_non_encrypted_at_rest_with_tags(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.kinesis_streams), 1)
        kinesis_stream = next((kinesis_stream for kinesis_stream in ctx.kinesis_streams
                               if kinesis_stream.stream_name == 'cloudrail-test-non-encrypted'), None)
        self.assertIsNotNone(kinesis_stream)
        self.assertTrue(kinesis_stream.tags)
