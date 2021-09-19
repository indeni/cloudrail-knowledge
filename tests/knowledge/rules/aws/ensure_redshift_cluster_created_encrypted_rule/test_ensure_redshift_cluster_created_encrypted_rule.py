from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_redshift_cluster_created_encrypted_rule import \
    EnsureRedshiftClusterCreatedEncryptedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureRedshiftClusterCreatedEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRedshiftClusterCreatedEncryptedRule()

    def test_encrypted_cluster(self):
        self.run_test_case('encrypted_cluster', False)

    def test_non_encrypted_cluster(self):
        self.run_test_case('non_encrypted_cluster', True)
