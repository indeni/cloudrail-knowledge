import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_s3_buckets_versioning_rule import EnsureS3BucketsVersioningRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.s3.s3_bucket_versioning import S3BucketVersioning


class TestEnsureS3BucketsVersioningRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketsVersioningRule()

    def test_not_car_s3_buckets_versioning_enabled_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        bucket_versioning: S3BucketVersioning = create_empty_entity(S3BucketVersioning)
        s3_bucket.versioning_data = bucket_versioning
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_s3_buckets_versioning_enabled_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        bucket_versioning: S3BucketVersioning = create_empty_entity(S3BucketVersioning)
        bucket_versioning.versioning = True
        s3_bucket.versioning_data = bucket_versioning
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
