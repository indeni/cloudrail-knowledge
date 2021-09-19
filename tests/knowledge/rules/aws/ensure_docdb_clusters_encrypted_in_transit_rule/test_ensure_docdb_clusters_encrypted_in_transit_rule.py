from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit.ensure_docdb_clusters_encrypted_in_transit_rule import \
    EnsureDocdbClustersEncryptedInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureDocdbClustersEncryptedInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedInTransitRule()

    def test_docdb_clusters_encrypted_in_transit(self):
        self.run_test_case('docdb_clusters_encrypted_in_transit', False)

    def test_docdb_clusters_non_encrypted_in_transit(self):
        self.run_test_case('docdb_clusters_non_encrypted_in_transit', True)
