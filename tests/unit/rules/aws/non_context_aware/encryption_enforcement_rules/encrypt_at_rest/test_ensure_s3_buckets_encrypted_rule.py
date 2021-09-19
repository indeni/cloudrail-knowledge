import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.connection import ConnectionDirectionType, ConnectionInstance, PolicyConnectionProperty, \
    PrivateConnectionDetail, \
    PublicConnectionDetail
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_encrypted_rule import \
    EnsureS3BucketsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureS3BucketsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketsEncryptedRule()

    def test_not_car_s3_buckets_encrypted_at_rest_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        terraform_state = create_empty_entity(IacState)
        s3_bucket.iac_state = terraform_state
        s3_bucket.iac_state.is_new = True
        s3_bucket.encryption_data = S3BucketEncryption(bucket_name='s3_bucket', encrypted=False, region='us-east-1', account='111111')
        connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
        s3_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_s3_buckets_encrypted_at_rest_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        terraform_state = create_empty_entity(IacState)
        s3_bucket.iac_state = terraform_state
        s3_bucket.iac_state.is_new = True
        s3_bucket.encryption_data = S3BucketEncryption(bucket_name='s3_bucket', encrypted=True, region='us-east-1', account='111111')
        connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
        s3_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_s3_buckets_encrypted_at_rest__public_conn__pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        terraform_state = create_empty_entity(IacState)
        s3_bucket.iac_state = terraform_state
        s3_bucket.iac_state.is_new = True
        s3_bucket.encryption_data = S3BucketEncryption(bucket_name='s3_bucket', encrypted=False, region='us-east-1', account='111111')
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)
        s3_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
