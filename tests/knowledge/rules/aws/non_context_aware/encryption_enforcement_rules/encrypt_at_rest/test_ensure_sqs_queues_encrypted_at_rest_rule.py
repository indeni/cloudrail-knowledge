import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_rule import \
    EnsureSqsQueuesEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSqsQueuesEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSqsQueuesEncryptedAtRestRule()

    def test_non_car_sqs_queue_encrypt_at_rest_fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = False
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sqs_queue_encrypt_at_rest_pass(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = True
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
