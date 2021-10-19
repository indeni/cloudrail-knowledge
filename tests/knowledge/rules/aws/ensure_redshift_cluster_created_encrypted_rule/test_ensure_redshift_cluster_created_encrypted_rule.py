from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_redshift_cluster_created_encrypted_rule import \
    EnsureRedshiftClusterCreatedEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureRedshiftClusterCreatedEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRedshiftClusterCreatedEncryptedRule()

    @rule_test('encrypted_cluster', False)
    def test_encrypted_cluster(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_cluster', True)
    def test_non_encrypted_cluster(self, rule_result: RuleResponse):
        pass
