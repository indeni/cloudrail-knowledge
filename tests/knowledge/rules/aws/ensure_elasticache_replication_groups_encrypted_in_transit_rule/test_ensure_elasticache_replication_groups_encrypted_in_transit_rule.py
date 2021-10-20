from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit\
    .ensure_elasticache_replication_groups_encrypted_in_transit_rule import \
    EnsureElasticacheReplicationGroupsEncryptedInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureElasticacheReplicationGroupsEncryptedInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheReplicationGroupsEncryptedInTransitRule()

    @rule_test('encrypted_in_transit', False)
    def test_encrypted_in_transit(self, rule_result: RuleResponse):
        pass

    @rule_test('no_encryption_at_rest', True)
    def test_no_encryption_at_rest(self, rule_result: RuleResponse):
        pass
