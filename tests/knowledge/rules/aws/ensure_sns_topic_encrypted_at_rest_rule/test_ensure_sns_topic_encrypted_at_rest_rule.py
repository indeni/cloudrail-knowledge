from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_rule import \
    EnsureSnsTopicEncryptedAtRestRule


class TestEnsureSnsTopicEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSnsTopicEncryptedAtRestRule()

    def test_not_encrypted_at_rest_2_units(self):
        self.run_test_case('not_encrypted_at_rest_2_units', True, 2)

    def test_encrypted_at_rest_alias(self):
        self.run_test_case('encrypted_at_rest_alias', False)
