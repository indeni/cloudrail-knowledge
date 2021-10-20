from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureSecretsManagerSecretPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSecretsManagerSecretPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSecretsManagerSecretPolicyNotUseWildcard()

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `secretsmanager:*`, and principal `AWS: *`, without any condition'
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Secrets Manager Secret')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Secrets Manager Secrets resource policy')

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass
