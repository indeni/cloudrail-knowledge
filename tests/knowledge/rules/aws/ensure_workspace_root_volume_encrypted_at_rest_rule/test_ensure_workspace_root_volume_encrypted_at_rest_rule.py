from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_root_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceRootVolumeEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureWorkspaceRootVolumeEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceRootVolumeEncryptedAtRestRule()

    @rule_test('root_volume_encrypted_at_rest', False)
    def test_root_volume_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('root_volume_not_encrypted_at_rest', True)
    def test_root_volume_not_encrypted_at_rest(self, rule_result: RuleResponse):
        pass
