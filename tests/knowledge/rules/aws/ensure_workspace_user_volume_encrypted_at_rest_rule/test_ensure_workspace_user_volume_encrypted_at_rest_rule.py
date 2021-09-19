from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_user_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureWorkspaceUserVolumeEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceUserVolumeEncryptedAtRestRule()

    def test_user_volume_encrypted_at_rest(self):
        self.run_test_case('user_volume_encrypted_at_rest', False)

    def test_user_volume_not_encrypted_at_rest(self):
        self.run_test_case('user_volume_not_encrypted_at_rest', True)
