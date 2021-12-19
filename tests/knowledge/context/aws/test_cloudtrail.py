from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestCloudTrail(AwsContextTest):

    def get_component(self):
        return "cloudtrail"

    # Not running drift test: as the KMS policy and S3 policy does not allow reading the KMS data, we have drift for missing entities.
    @context(module_path="encrypted", test_options=TestOptions(run_drift_detection=False))
    def test_encrypted(self, ctx: AwsEnvironmentContext):
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-kms-cmk-encryption'), None)
        self.assertIsNotNone(trail)
        self.assertTrue(trail.kms_encryption)
        self.assertTrue(trail.arn)
        self.assertFalse(trail.log_file_validation)
        self.assertFalse(trail.is_multi_region_trail)
        if not trail.is_managed_by_iac:
            self.assertEqual(trail.get_cloud_resource_url(), 'https://console.aws.amazon.com/cloudtrail/home?region=us-east-1#/trails/'
                                                             'arn:aws:cloudtrail:us-east-1:115553109071:trail/cloudtrail-logs-kms-cmk-encryption')

    @context(module_path="non_encrypted")
    def test_non_encrypted(self, ctx: AwsEnvironmentContext):
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-default-encryption'), None)
        self.assertIsNotNone(trail)
        self.assertFalse(trail.kms_encryption)
        self.assertTrue(trail.arn)
        self.assertFalse(trail.log_file_validation)
        self.assertFalse(trail.tags)

    @context(module_path="file_log_validation_enabled")
    def test_file_log_validation_enabled(self, ctx: AwsEnvironmentContext):
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-default-encryption'), None)
        self.assertIsNotNone(trail)
        self.assertFalse(trail.kms_encryption)
        self.assertTrue(trail.arn)
        self.assertTrue(trail.log_file_validation)

    @context(module_path="with_tags")
    def test_with_tags(self, ctx: AwsEnvironmentContext):
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-default-encryption'), None)
        self.assertIsNotNone(trail)
        self.assertTrue(trail.tags)

    @context(module_path="multi-region-enabled")
    def test_multi_region_enabled(self, ctx: AwsEnvironmentContext):
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'test-trail-multiregion-enabled'), None)
        self.assertIsNotNone(trail)
        self.assertTrue(trail.is_multi_region_trail)

    @context(module_path="cloudtrail_with_similar_tags")
    def test_cloudtrail_with_similar_tags(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.cloudtrail) > 1)
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-default-encryption'), None)
        self.assertIsNotNone(trail)
        self.assertTrue(trail.tags)
        self.assertEqual(trail.tags['Name'], 'Cloudtrail-test')
        trail = next((trail for trail in ctx.cloudtrail if trail.server_name == 'cloudtrail-logs-default-encryption-2'), None)
        self.assertIsNotNone(trail)
        self.assertTrue(trail.tags)
        self.assertEqual(trail.tags['Name'], 'Cloudtrail-test-2')
