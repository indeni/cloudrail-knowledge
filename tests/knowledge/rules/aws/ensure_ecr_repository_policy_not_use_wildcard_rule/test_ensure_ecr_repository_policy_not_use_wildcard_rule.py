from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureEcrRepositoryPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEcrRepositoryPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoryPolicyNotUseWildcard()

    @rule_test('non_secure_policy', True)
    def test_non_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `ecr:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'ECR repository')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'ECR repository resource policy')

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass
