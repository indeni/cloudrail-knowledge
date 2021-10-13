from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_root_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceRootVolumeEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureWorkspaceRootVolumeEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceRootVolumeEncryptedAtRestRule()

    def test_root_volume_encrypted_at_rest(self):
        self.run_test_case('root_volume_encrypted_at_rest', False)

    def test_root_volume_not_encrypted_at_rest(self):
        self.run_test_case('root_volume_not_encrypted_at_rest', True)
