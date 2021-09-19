from typing import Dict

from cloudrail.knowledge.context.connection import PolicyEvaluation, PrivateConnectionDetail, ConnectionType
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.policy_evaluator import is_any_action_allowed

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestS3Bucket(AwsContextTest):

    def get_component(self):
        return "s3_bucket"

    @context(module_path="s3-bucket-permissions-connections")
    def test_s3_bucket_permissions_connections(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(next(iter(ctx.s3_buckets)).inbound_connections), 1)
        private_conn: PrivateConnectionDetail = next(iter(next(iter(ctx.s3_buckets)).inbound_connections))
        self.assertEqual(private_conn.connection_type, ConnectionType.PRIVATE)
        self.assertEqual(private_conn.target_instance, ctx.roles[0])
        self.assertEqual(len(private_conn.connection_property.policy_evaluation), 1)
        policy_eval: PolicyEvaluation = private_conn.connection_property.policy_evaluation[0]
        self.assertTrue(is_any_action_allowed(policy_eval))

    @context(module_path="s3-bucket-permissions-connections")
    def test_role_to_s3_bucket_permissions(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.roles[0].policy_evaluation_result_map), 1)
        bucket: S3Bucket = next(iter(ctx.s3_buckets))
        eval_map: Dict[str, PolicyEvaluation] = ctx.roles[0].policy_evaluation_result_map
        self.assertIsNotNone(eval_map.get(bucket.arn, None))
        policy_eval: PolicyEvaluation = eval_map[bucket.arn]
        self.assertTrue(is_any_action_allowed(policy_eval))

    @context(module_path="bucket_and_object_with_tags")
    def test_bucket_with_tags(self, ctx: AwsEnvironmentContext):
        bucket = next((bucket for bucket in ctx.s3_buckets if bucket.bucket_name == 'cloudrail-non-encrypted-czx7zxchs'), None)
        self.assertTrue(bucket)
        self.assertEqual(bucket.tags, {'Name': 'S3-bucket-testing-tags'})
        self.assertEqual(bucket.get_cloud_resource_url(),
                         'https://s3.console.aws.amazon.com/s3/buckets/cloudrail-non-encrypted-czx7zxchs?region=us-east-1&tab=objects')

    @context(module_path="bucket_and_object_with_tags", test_options=TestOptions(run_cloudmapper=False))
    def test_object_with_tags(self, ctx: AwsEnvironmentContext):
        bucket_object = next((s3_object for s3_object in ctx.s3_bucket_objects
                              if s3_object.key == 'example_file_non_encrypted'), None)
        self.assertTrue(bucket_object)
        self.assertTrue(bucket_object.tags)
        if not bucket_object.is_managed_by_iac:
            self.assertEqual(bucket_object.get_cloud_resource_url(),
                             'https://s3.console.aws.amazon.com/s3/object/'
                             'cloudrail-non-encrypted-czx7zxchs?region=us-east-1&prefix=example_file_non_encrypted')
