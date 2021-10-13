from typing import List
from cloudrail.knowledge.context.connection import ConnectionDetail, ConnectionType
from cloudrail.knowledge.context.aws.resources.cloudfront.cloud_front_distribution_list import CloudFrontDistribution
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.policy_evaluator import is_any_action_allowed

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestCloudFrontDistributionList(AwsContextTest):

    def get_component(self):
        return 'cloudfront_distribution_list'
    # Not running drift as unable to create drift data - need live DNS to authorize certificate
    @context(module_path="basic", test_options=TestOptions(run_drift_detection=False))
    def test_basic(self, ctx: AwsEnvironmentContext):
        distribution = ctx.cloudfront_distribution_list[0]
        if distribution.is_managed_by_iac:
            self.assertEqual(distribution.arn, 'aws_cloudfront_distribution.s3_distribution.arn')
            self.assertEqual(distribution.name, 'aws_cloudfront_distribution.s3_distribution.domain_name')
            self.assertTrue(distribution.distribution_id, 'aws_cloudfront_distribution.s3_distribution.id')
        else:
            self.assertEqual(distribution.arn, 'arn:aws:cloudfront::111111111111:distribution/E1IT85M7RP5KK4')
            self.assertEqual(distribution.name, 'de2tklz10ets5.cloudfront.net')
            self.assertTrue(distribution.distribution_id, 'E1IT85M7RP5KK4')
            self.assertEqual(distribution.get_cloud_resource_url(), 'https://console.aws.amazon.com/cloudfront/'
                                                                    'home?region=us-east-1#distribution-settings:E1IT85M7RP5KK4')
        self.assertEqual(distribution.viewer_cert.minimum_protocol_version, 'TLSv1')

    @context(module_path="protocol_viewer_policy_allow_all")
    def test_protocol_viewer_policy_allow_all(self, ctx: AwsEnvironmentContext):
        distribution = ctx.cloudfront_distribution_list[0]
        self.assertEqual(distribution.get_default_behavior().viewer_protocol_policy, 'allow-all')
        self.assertTrue(len(distribution.get_ordered_behavior_list()) == 2)
        self.assertEqual(distribution.get_ordered_behavior_list()[0].viewer_protocol_policy, 'allow-all')
        self.assertFalse(distribution.get_default_behavior().field_level_encryption_id)
        self.assertTrue(len(distribution.get_ordered_behavior_list()) == 2)

    # Not running drift as unable to create drift data - need live DNS to authorize certificate
    @context(module_path="field_level_encryption_enabled", base_scanner_data_for_iac='account-data-cloudfront-field-level-encryption',
             test_options=TestOptions(run_drift_detection=False))
    def test_field_level_encryption_enabled(self, ctx: AwsEnvironmentContext):
        distribution = ctx.cloudfront_distribution_list[0]
        self.assertTrue(distribution.get_default_behavior().field_level_encryption_id)
        self.assertTrue(len(distribution.get_ordered_behavior_list()) == 2)

    @context(module_path="aoi-restrict-public-access")
    def test_aoi_restrict_public_access(self, ctx: AwsEnvironmentContext):
        self.assert_aoi_restrict_access(ctx.cloudfront_distribution_list)
        cloudfront: CloudFrontDistribution = ctx.cloudfront_distribution_list[0]
        self.assertEqual(len(cloudfront.inbound_connections), 1)
        conn_detail = next(iter(cloudfront.inbound_connections))
        self.assertEqual(conn_detail.connection_type, ConnectionType.PUBLIC)

    @context(module_path="aoi-restrict-private-access")
    def test_aoi_restrict_private_access(self, ctx: AwsEnvironmentContext):
        conn_detail = self.assert_aoi_restrict_access(ctx.cloudfront_distribution_list)
        self.assertEqual(len(ctx.cloudfront_distribution_list), 1)

        bucket: S3Bucket = ctx.s3_buckets.get('static-web-resources-bucket-cloudrail-aoi-private-test')
        self.assertIsNotNone(bucket)
        self.assertEqual(conn_detail.target_instance, bucket)
        self.assertEqual(len(bucket.inbound_connections), 1)

    def assert_aoi_restrict_access(self, cloudfront_distribution_list: List[CloudFrontDistribution]) -> ConnectionDetail:
        self.assertEqual(len(cloudfront_distribution_list), 1)
        cloudfront: CloudFrontDistribution = cloudfront_distribution_list[0]
        self.assertEqual(len(cloudfront.outbound_connections), 1)
        conn_detail = next(iter(cloudfront.outbound_connections))
        self.assertEqual(len(conn_detail.connection_property.policy_evaluation), 1)
        self.assertTrue(is_any_action_allowed(conn_detail.connection_property.policy_evaluation[0]))
        return conn_detail

    @context(module_path="waf_enabled")
    def test_waf_enabled(self, ctx: AwsEnvironmentContext):
        cloudfront = next((cloudfront for cloudfront in ctx.cloudfront_distribution_list
                           if cloudfront.name == 'd57np39wjyiiz.cloudfront.net'
                           or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront)
        self.assertTrue(cloudfront.web_acl_id)
        self.assertTrue(cloudfront.is_waf_enabled)

    @context(module_path="waf_disabled")
    def test_waf_disabled(self, ctx: AwsEnvironmentContext):
        cloudfront = next((cloudfront for cloudfront in ctx.cloudfront_distribution_list
                           if cloudfront.name == 'd2d7f93b8bzkct.cloudfront.net'
                           or cloudfront.name == 'aws_cloudfront_distribution.s3_distribution.domain_name'), None)
        self.assertIsNotNone(cloudfront)
        self.assertFalse(cloudfront.is_waf_enabled)
