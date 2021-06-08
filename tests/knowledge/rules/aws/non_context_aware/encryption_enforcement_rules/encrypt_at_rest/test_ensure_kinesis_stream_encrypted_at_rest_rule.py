import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_kinesis_stream_encrypted_at_rest_rule import EnsureKinesisStreamEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureKinesisStreamEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureKinesisStreamEncryptedAtRestRule()

    def test_non_car_kinesis_stream_encrypt_at_rest_fail(self):
        # Arrange
        kinesis_stream: KinesisStream = create_empty_entity(KinesisStream)
        kinesis_stream.encrypted_at_rest = False
        context = AwsEnvironmentContext(kinesis_streams=[kinesis_stream])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_kinesis_stream_encrypt_at_rest_pass(self):
        # Arrange
        kinesis_stream: KinesisStream = create_empty_entity(KinesisStream)
        kinesis_stream.encrypted_at_rest = True
        context = AwsEnvironmentContext(kinesis_streams=[kinesis_stream])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
