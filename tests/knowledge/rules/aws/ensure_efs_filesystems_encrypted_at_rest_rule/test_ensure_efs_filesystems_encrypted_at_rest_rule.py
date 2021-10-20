from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_efs_filesystems_encrypted_at_rest_rule import\
    EnsureEfsFilesystemsEncryptedAtRestRule


class TestEnsureEfsFilesystemsEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEfsFilesystemsEncryptedAtRestRule()

    @rule_test('efs_encrypted', False)
    def test_efs_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        pass
