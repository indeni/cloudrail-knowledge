from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit\
    .ensure_elasticache_replication_groups_encrypted_in_transit_rule import \
    EnsureElasticacheReplicationGroupsEncryptedInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureElasticacheReplicationGroupsEncryptedInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheReplicationGroupsEncryptedInTransitRule()

    def test_encrypted_in_transit(self):
        self.run_test_case('encrypted_in_transit', False)

    def test_no_encryption_at_rest(self):
        self.run_test_case('no_encryption_at_rest', True)
