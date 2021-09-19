import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_s3_bucket_logging_enabled_rule import \
    EnsureS3BucketLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureS3BucketLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketLoggingEnabledRule()

    def test_non_car_s3_bucket_access_logging_enabled_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.iac_state = IacState('dummy_path', IacActionType.CREATE, None, True)
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_s3_bucket_access_logging_enabled_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket_log: S3BucketLogging = create_empty_entity(S3BucketLogging)
        s3_bucket_log.target_bucket = 'some_s3_arn'
        s3_bucket.bucket_logging = s3_bucket_log
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_s3_bucket_access_not_logging_enabled_as_logger(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.is_logger = True
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
