
import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL, S3Permission
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.s3_acl_allow_public_access_rule import S3AclAllowPublicAccessRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestS3AclAllowPublicAccessRule(unittest.TestCase):
    def setUp(self):
        self.rule = S3AclAllowPublicAccessRule()

    def test_s3_acl_disallow_public_and_cross_account_fail(self):
        # Arrange
        bucket = create_empty_entity(S3Bucket, bucket_name='bucket_name')
        s3acl = create_empty_entity(S3ACL, s3_permission=S3Permission.READ)
        bucket.publicly_allowing_resources.append(s3acl)
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_s3_acl_disallow_public_and_cross_account_pass(self):
        # Arrange
        bucket = create_empty_entity(S3Bucket, bucket_name='bucket_name')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
