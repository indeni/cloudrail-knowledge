from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_database_encrypted_at_rest_rule import \
    EnsureAthenaDatabaseEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureAthenaDatabaseEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAthenaDatabaseEncryptedAtRestRule()

    @rule_test('encrypted', False)
    def test_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('not_encrypted', True)
    def test_not_encrypted(self, rule_result: RuleResponse):
        pass
