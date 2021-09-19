from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestCloudFrontDistributionLogging(AwsContextTest):

    def get_component(self):
        return 'cloudfront_distribution_logging'

    @context(module_path="with_logging_access_enabled")
    def test_with_logging_access_enabled(self, ctx: AwsEnvironmentContext):
        cloudfront = next((cloudfront for cloudfront in ctx.cloudfront_log_settings
                           if cloudfront.name == 'dup2qudpsojs0.cloudfront.net'
                           or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront)
        self.assertTrue(cloudfront.distribution_id)
        self.assertTrue(cloudfront.arn)
        self.assertTrue(cloudfront.logging_enabled)
        self.assertTrue(cloudfront.s3_bucket)
        self.assertEqual(cloudfront.prefix, 'myprefix')
        self.assertFalse(cloudfront.include_cookies)
        cloudfront_dist = next((cloudfront for cloudfront in ctx.cloudfront_distribution_list
                                if cloudfront.name == 'dup2qudpsojs0.cloudfront.net'
                                or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront_dist)
        self.assertTrue(cloudfront_dist.logs_settings)
        self.assertTrue(cloudfront_dist.logs_settings.logging_enabled)

    @context(module_path="logging_enabled_basic_config")
    def test_logging_enabled_basic_config(self, ctx: AwsEnvironmentContext):
        cloudfront = next((cloudfront for cloudfront in ctx.cloudfront_log_settings
                           if cloudfront.name == 'd10vu83o5lodi4.cloudfront.net'
                           or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront)
        self.assertTrue(cloudfront.distribution_id)
        self.assertTrue(cloudfront.arn)
        self.assertTrue(cloudfront.logging_enabled)
        self.assertTrue(cloudfront.s3_bucket)
        self.assertFalse(cloudfront.prefix)
        self.assertFalse(cloudfront.include_cookies)

    @context(module_path="no_logging_at_all")
    def test_no_logging_at_all(self, ctx: AwsEnvironmentContext):
        cloudfront = next((cloudfront for cloudfront in ctx.cloudfront_log_settings
                           if cloudfront.name == 'd2h40sipo10d74.cloudfront.net'
                           or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront)
        self.assertTrue(cloudfront.distribution_id)
        self.assertTrue(cloudfront.arn)
        self.assertFalse(cloudfront.logging_enabled)
        self.assertFalse(cloudfront.s3_bucket)
        self.assertFalse(cloudfront.prefix)
        self.assertFalse(cloudfront.include_cookies)
