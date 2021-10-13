from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import EnsureEfsPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEfsPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEfsPolicyNotUseWildcard()

    def test_not_secure_action_and_principal_secure_condition(self):
        self.run_test_case('not_secure_action_and_principal_secure_condition', False)

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `elasticfilesystem:*`, and principal `AWS: *`, without any condition'
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Elastic File System')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'EFS file system resource policy')
