from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.policy_wildcard_violation_rules import EnsureEfsPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEfsPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEfsPolicyNotUseWildcard()

    @rule_test('not_secure_action_and_principal_secure_condition', False)
    def test_not_secure_action_and_principal_secure_condition(self, rule_result: RuleResponse):
        pass

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `elasticfilesystem:*`, and principal `AWS: *`, without any condition'
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Elastic File System')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'EFS file system resource policy')
