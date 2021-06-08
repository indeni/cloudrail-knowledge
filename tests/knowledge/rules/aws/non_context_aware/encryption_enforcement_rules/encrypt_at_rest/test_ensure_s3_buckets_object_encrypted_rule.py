import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.aws_connection import ConnectionDirectionType, ConnectionInstance, PolicyConnectionProperty, \
    PrivateConnectionDetail, PublicConnectionDetail
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_object_encrypted_rule import \
    EnsureS3BucketObjectsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureS3BucketObjectsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketObjectsEncryptedRule()

    def test_not_car_s3_bucket_object_encrypt_at_rest_fail(self):
        # Arrange
        s3_bucket_object: S3BucketObject = create_empty_entity(S3BucketObject)
        s3_bucket_object.encrypted = False
        s3_bucket_object.owning_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
        s3_bucket_object.owning_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_bucket_objects=[s3_bucket_object])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_s3_bucket_object_encrypt_at_rest_pass(self):
        # Arrange
        s3_bucket_object: S3BucketObject = create_empty_entity(S3BucketObject)
        s3_bucket_object.encrypted = True
        s3_bucket_object.owning_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
        s3_bucket_object.owning_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_bucket_objects=[s3_bucket_object])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_s3_bucket_object_encrypt_at_rest__no_inbound_public__pass(self):
        # Arrange
        s3_bucket_object: S3BucketObject = create_empty_entity(S3BucketObject)
        s3_bucket_object.encrypted = False
        s3_bucket_object.owning_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)
        s3_bucket_object.owning_bucket.inbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(s3_bucket_objects=[s3_bucket_object])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
