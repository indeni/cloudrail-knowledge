from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_neptune_cluster_encrypted_at_rest_rule import \
    EnsureNeptuneClusterEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureNeptuneClusterEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterEncryptedAtRestRule()

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)

    def test_not_encrypted_at_rest(self):
        self.run_test_case('not_encrypted_at_rest', True)
