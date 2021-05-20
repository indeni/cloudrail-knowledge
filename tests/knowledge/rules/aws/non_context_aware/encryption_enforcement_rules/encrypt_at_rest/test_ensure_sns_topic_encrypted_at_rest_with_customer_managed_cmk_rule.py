import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_with_customer_managed_cmk_rule import EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule()

    def test_non_car_sns_topics_encrypted_at_rest_with_customer_managed_cmk_fail(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = True
        sns_topic.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sns_topics_encrypted_at_rest_with_customer_managed_cmk__no_kms_data__fail(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = True
        sns_topic.kms_data = None
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sns_topics_encrypted_at_rest_with_customer_managed_cmk_pass(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = True
        sns_topic.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_sns_topics_encrypted_at_rest_with_customer_managed_cmk__noe_encryption__pass(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = False
        sns_topic.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
