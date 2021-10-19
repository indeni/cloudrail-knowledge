from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit.ensure_docdb_clusters_encrypted_in_transit_rule import \
    EnsureDocdbClustersEncryptedInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureDocdbClustersEncryptedInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedInTransitRule()

    @rule_test('docdb_clusters_encrypted_in_transit', False)
    def test_docdb_clusters_encrypted_in_transit(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_clusters_non_encrypted_in_transit', True)
    def test_docdb_clusters_non_encrypted_in_transit(self, rule_result: RuleResponse):
        pass
