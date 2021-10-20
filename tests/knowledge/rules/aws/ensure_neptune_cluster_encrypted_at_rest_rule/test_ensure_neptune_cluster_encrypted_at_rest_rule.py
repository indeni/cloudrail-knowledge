from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_neptune_cluster_encrypted_at_rest_rule import \
    EnsureNeptuneClusterEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureNeptuneClusterEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterEncryptedAtRestRule()

    @rule_test('encrypted_at_rest', False)
    def test_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('not_encrypted_at_rest', True)
    def test_not_encrypted_at_rest(self, rule_result: RuleResponse):
        pass
