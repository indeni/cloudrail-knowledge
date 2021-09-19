import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_with_customer_managed_cmk_rule import EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule()

    def test_non_car_sqs_queues_encrypted_at_rest_with_customer_managed_cmk_fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = True
        sqs_queue.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sqs_queues_encrypted_at_rest_with_customer_managed_cmk__no_kms_data__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = True
        sqs_queue.kms_data = None
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sqs_queues_encrypted_at_rest_with_customer_managed_cmk_pass(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = True
        sqs_queue.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_sqs_queues_encrypted_at_rest_with_customer_managed_cmk__no_encrypt__pass(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.encrypted_at_rest = False
        sqs_queue.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
