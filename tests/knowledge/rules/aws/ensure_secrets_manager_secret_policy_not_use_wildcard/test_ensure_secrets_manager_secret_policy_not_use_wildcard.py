from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureSecretsManagerSecretPolicyNotUseWildcard
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSecretsManagerSecretPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSecretsManagerSecretPolicyNotUseWildcard()

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `secretsmanager:*`, and principal `AWS: *`, without any condition'
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Secrets Manager Secret')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Secrets Manager Secrets resource policy')

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)
