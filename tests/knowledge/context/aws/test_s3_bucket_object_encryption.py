from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestS3BucketObjectEncryption(AwsContextTest):

    def get_component(self):
        return "s3_bucket_object"

    @context(module_path="encrypted_aes256", test_options=TestOptions(run_cloudmapper=False))
    def test_encrypted_aes256(self, ctx: AwsEnvironmentContext):
        for s3_bucket_object in ctx.s3_bucket_objects:
            if s3_bucket_object.bucket_name == 'cloudrail':
                self.assertTrue(s3_bucket_object.encrypted)
                self.assertEqual(s3_bucket_object.key, 'example_file_encrypted_aes256')

    @context(module_path="encrypted_aws_kms", test_options=TestOptions(run_cloudmapper=False))
    def test_encrypted_aws_kms(self, ctx: AwsEnvironmentContext):
        for s3_bucket_object in ctx.s3_bucket_objects:
            if s3_bucket_object.bucket_name == 'cloudrail':
                self.assertTrue(s3_bucket_object.encrypted)

    @context(module_path="non_encrypted", test_options=TestOptions(run_cloudmapper=False))
    def test_non_encrypted(self, ctx: AwsEnvironmentContext):
        for s3_bucket_object in ctx.s3_buckets:
            if s3_bucket_object.bucket_name == 'cloudrail':
                self.assertFalse(s3_bucket_object.encrypted)
