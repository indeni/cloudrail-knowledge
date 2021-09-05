from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureEcrRepositoryPolicyNotUseWildcard
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcrRepositoryPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoryPolicyNotUseWildcard()

    def test_non_secure_policy(self):
        rule_result = self.run_test_case('non_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `ecr:*`, and principal `AWS: *`, without any condition' in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'ECR repository')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'ECR repository resource policy')

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)
