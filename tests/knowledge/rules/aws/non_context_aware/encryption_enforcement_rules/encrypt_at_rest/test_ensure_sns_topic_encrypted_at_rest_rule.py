import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_rule import \
    EnsureSnsTopicEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSnsTopicEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSnsTopicEncryptedAtRestRule()

    def test_non_car_sns_topic_encrypt_at_rest_fail(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = False
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sns_topic_encrypt_at_rest_pass(self):
        # Arrange
        sns_topic: SnsTopic = create_empty_entity(SnsTopic)
        sns_topic.encrypted_at_rest = True
        context = EnvironmentContext(sns_topics=[sns_topic])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
