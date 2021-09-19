from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dax_clusters_encrypted_rule import \
    EnsureDaxClustersEncryptedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureDaxClustersEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDaxClustersEncryptedRule()

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)

    def test_non_encrypted_cluster(self):
        self.run_test_case('non_encrypted_cluster', True)
