from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_elasticache_replication_groups_encrypted_at_rest_rule \
    import EnsureElasticacheReplicationGroupsEncryptedAtRestRule


class TestEnsureElasticacheReplicationGroupsEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheReplicationGroupsEncryptedAtRestRule()

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)

    def test_no_encryption_at_rest(self):
        self.run_test_case('no_encryption_at_rest', True)
