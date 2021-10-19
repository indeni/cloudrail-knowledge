from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_rule import \
    EnsureDocdbClustersEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureDocdbClustersEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedRule()

    @rule_test('docdb_clusters_encrypted_at_rest', False)
    def test_docdb_clusters_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_clusters_non_encrypted', True)
    def test_docdb_clusters_non_encrypted(self, rule_result: RuleResponse):
        pass
