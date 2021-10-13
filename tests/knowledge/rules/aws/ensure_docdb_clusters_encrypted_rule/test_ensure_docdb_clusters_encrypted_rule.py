from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_rule import \
    EnsureDocdbClustersEncryptedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureDocdbClustersEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedRule()

    def test_docdb_clusters_encrypted_at_rest(self):
        self.run_test_case('docdb_clusters_encrypted_at_rest', False)

    def test_docdb_clusters_non_encrypted(self):
        self.run_test_case('docdb_clusters_non_encrypted', True)
