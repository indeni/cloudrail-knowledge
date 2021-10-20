from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_managed_disks_encrypted_rule import EnsureManagedDisksEncryptedRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureManagedDisksEncryptedRule(AzureBaseRuleTest):

    def get_rule(self):
        return EnsureManagedDisksEncryptedRule()

    @rule_test('encrypted_with_disk_encryption_set_resource', False)
    def test_encrypted_with_disk_encryption_set_resource(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_with_encryption_settings', False)
    def test_encrypted_with_encryption_settings(self, rule_result: RuleResponse):
        pass

    @rule_test('not_encrypted_disk', True)
    def test_not_encrypted_disk(self, rule_result: RuleResponse):
        pass
