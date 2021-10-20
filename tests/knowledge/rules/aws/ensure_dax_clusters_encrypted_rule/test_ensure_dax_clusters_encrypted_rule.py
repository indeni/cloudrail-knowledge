from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dax_clusters_encrypted_rule import \
    EnsureDaxClustersEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureDaxClustersEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDaxClustersEncryptedRule()

    @rule_test('encrypted_at_rest', False)
    def test_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_cluster', True)
    def test_non_encrypted_cluster(self, rule_result: RuleResponse):
        pass
