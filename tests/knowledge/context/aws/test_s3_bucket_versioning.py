from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestS3BucketVersioning(AwsContextTest):

    def get_component(self):
        return "s3_bucket"

    @context(module_path="versioning_enabled")
    def test_versioning_enabled(self, ctx: AwsEnvironmentContext):
        self._versioning_mode(ctx, True)

    @context(module_path="versioning_disabled")
    def test_versioning_disabled(self, ctx: AwsEnvironmentContext):
        self._versioning_mode(ctx, False)

    def _versioning_mode(self, ctx: AwsEnvironmentContext, enabled: bool):
        self.assertGreater(len(ctx.s3_buckets), 0)
        found: bool = False
        for s3_bucket in ctx.s3_buckets:
            if s3_bucket.versioning_data.bucket_name == 'my-tf-test-bucket5656':
                self.assertEqual(s3_bucket.versioning_data.versioning, enabled)
                found = True
        self.assertTrue(found, 'bucket=my-tf-test-bucket5656 not found')
