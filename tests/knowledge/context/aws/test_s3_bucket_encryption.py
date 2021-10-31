from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestS3BucketEncryption(AwsContextTest):

    def get_component(self):
        return "s3_bucket"

    @context(module_path="encrypted-v1")
    def test_encrypted(self, ctx: AwsEnvironmentContext):
        for s3_bucket in ctx.s3_buckets:
            if s3_bucket.encryption_data.bucket_name == 'cloudrail-encrypted-czx7zxchs':
                self.assertTrue(s3_bucket.encryption_data.encrypted)
                break

    @context(module_path="non_encrypted")
    def test_non_encrypted(self, ctx: AwsEnvironmentContext):
        for s3_bucket in ctx.s3_buckets:
            if s3_bucket.encryption_data.bucket_name == 'cloudrail-non-encrypted-czx7zxchs':
                self.assertFalse(s3_bucket.encryption_data.encrypted)
                break
