from cloudrail.knowledge.rules.azure.non_context_aware.ensure_managed_disks_encrypted_rule import EnsureManagedDisksEncryptedRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestEnsureManagedDisksEncryptedRule(AzureBaseRuleTest):

    def get_rule(self):
        return EnsureManagedDisksEncryptedRule()

    def test_encrypted_with_disk_encryption_set_resource(self):
        self.run_test_case('encrypted_with_disk_encryption_set_resource', False)

    def test_encrypted_with_encryption_settings(self):
        self.run_test_case('encrypted_with_encryption_settings', False)

    def test_not_encrypted_disk(self):
        self.run_test_case('not_encrypted_disk', True)
