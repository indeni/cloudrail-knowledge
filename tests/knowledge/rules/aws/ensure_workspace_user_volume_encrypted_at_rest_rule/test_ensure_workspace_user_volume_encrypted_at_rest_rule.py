from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_user_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureWorkspaceUserVolumeEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceUserVolumeEncryptedAtRestRule()

    @rule_test('user_volume_encrypted_at_rest', False)
    def test_user_volume_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('user_volume_not_encrypted_at_rest', True)
    def test_user_volume_not_encrypted_at_rest(self, rule_result: RuleResponse):
        pass
