from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_elasticache_replication_groups_encrypted_at_rest_rule \
    import EnsureElasticacheReplicationGroupsEncryptedAtRestRule


class TestEnsureElasticacheReplicationGroupsEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheReplicationGroupsEncryptedAtRestRule()

    @rule_test('encrypted_at_rest', False)
    def test_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('no_encryption_at_rest', True)
    def test_no_encryption_at_rest(self, rule_result: RuleResponse):
        pass
