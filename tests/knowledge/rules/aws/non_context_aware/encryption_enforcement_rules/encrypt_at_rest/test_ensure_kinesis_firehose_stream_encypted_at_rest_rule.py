import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_kinesis_firehose_stream_encypted_at_rest_rule import EnsureKinesisFirehoseStreamEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureKinesisFirehoseStreamEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureKinesisFirehoseStreamEncryptedAtRestRule()

    def test_non_car_kinesis_firehose_delivery_stream_encrypt_at_rest_fail(self):
        # Arrange
        kinesis_firehose_stream: KinesisFirehoseStream = create_empty_entity(KinesisFirehoseStream)
        kinesis_firehose_stream.encrypted_at_rest = False
        context = EnvironmentContext(kinesis_firehose_streams=[kinesis_firehose_stream])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_kinesis_firehose_delivery_stream_encrypt_at_rest_pass(self):
        # Arrange
        kinesis_firehose_stream: KinesisFirehoseStream = create_empty_entity(KinesisFirehoseStream)
        kinesis_firehose_stream.encrypted_at_rest = True
        context = EnvironmentContext(kinesis_firehose_streams=[kinesis_firehose_stream])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
