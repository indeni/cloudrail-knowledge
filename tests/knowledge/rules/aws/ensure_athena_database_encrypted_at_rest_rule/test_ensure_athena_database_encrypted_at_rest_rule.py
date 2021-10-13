from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_database_encrypted_at_rest_rule import \
    EnsureAthenaDatabaseEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureAthenaDatabaseEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAthenaDatabaseEncryptedAtRestRule()

    def test_encrypted(self):
        self.run_test_case('encrypted', False)

    def test_not_encrypted(self):
        self.run_test_case('not_encrypted', True)
