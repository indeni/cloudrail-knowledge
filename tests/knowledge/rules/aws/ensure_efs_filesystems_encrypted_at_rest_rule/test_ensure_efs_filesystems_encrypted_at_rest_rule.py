from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_efs_filesystems_encrypted_at_rest_rule import\
    EnsureEfsFilesystemsEncryptedAtRestRule


class TestEnsureEfsFilesystemsEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEfsFilesystemsEncryptedAtRestRule()

    def test_efs_encrypted(self):
        self.run_test_case('efs_encrypted', False)

    def test_not_secure_policy(self):
        self.run_test_case('not_secure_policy', True)
