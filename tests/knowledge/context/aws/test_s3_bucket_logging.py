from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestS3BucketLogging(AwsContextTest):

    def get_component(self):
        return "s3_bucket"

    @context(module_path="with_logging")
    def test_logging_configuration(self, ctx: AwsEnvironmentContext):
        s3_bucket_logging = next((s3 for s3 in ctx.s3_bucket_logs
                                  if self._is_source_bucket(s3.bucket_name)), None)
        self.assertIsNotNone(s3_bucket_logging)
        self.assertTrue(s3_bucket_logging.target_bucket)
        self.assertEqual(s3_bucket_logging.target_prefix, 'log/')
        s3_bucket = next((s3 for s3 in ctx.s3_buckets
                          if self._is_source_bucket(s3.bucket_name)), None)
        self.assertIsNotNone(s3_bucket)
        self.assertTrue(s3_bucket.bucket_logging)
        self.assertTrue(s3_bucket.bucket_logging.target_bucket)
        self.assertEqual(s3_bucket.bucket_logging.target_prefix, 'log/')
        self.assertFalse(s3_bucket.is_logger)

    @staticmethod
    def _is_source_bucket(bucket_name: str) -> bool:
        return bucket_name in ('aws_s3_bucket.test.bucket', 'terraform-20210603113943203800000002', 'SourceBucket')
