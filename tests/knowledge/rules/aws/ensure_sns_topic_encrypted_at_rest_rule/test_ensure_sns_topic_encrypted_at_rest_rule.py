from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_rule import \
    EnsureSnsTopicEncryptedAtRestRule


class TestEnsureSnsTopicEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSnsTopicEncryptedAtRestRule()

    @rule_test('not_encrypted_at_rest_2_units', True, 2)
    def test_not_encrypted_at_rest_2_units(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_at_rest_alias', False)
    def test_encrypted_at_rest_alias(self, rule_result: RuleResponse):
        pass
