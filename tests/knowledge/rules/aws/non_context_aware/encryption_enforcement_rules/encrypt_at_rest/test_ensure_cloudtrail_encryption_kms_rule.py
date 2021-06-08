import unittest

from cloudrail.knowledge.context.aws.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloudtrail_encryption_kms_rule import \
    EnsureCloudTrailEncryptionKmsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureCloudTrailEncryptionKmsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudTrailEncryptionKmsRule()

    def test_not_car_cloudtrail_trails_encrypt_at_rest_with_sse_kms_fail(self):
        # Arrange
        cloudtrail: CloudTrail = create_empty_entity(CloudTrail)
        cloudtrail.kms_encryption = False

        context = AwsEnvironmentContext(cloudtrail=[cloudtrail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_cloudtrail_trails_encrypt_at_rest_with_sse_kms_pass(self):
        # Arrange
        cloudtrail: CloudTrail = create_empty_entity(CloudTrail)
        cloudtrail.kms_encryption = True

        context = AwsEnvironmentContext(cloudtrail=[cloudtrail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
