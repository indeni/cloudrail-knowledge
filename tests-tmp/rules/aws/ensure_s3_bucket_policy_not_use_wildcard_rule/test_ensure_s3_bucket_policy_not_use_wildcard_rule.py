from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureS3BucketPolicyNotUseWildcard
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureS3BucketPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketPolicyNotUseWildcard()

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_action_principal_and_condition_secure(self):
        self.run_test_case('not_secure_action_principal_and_condition_secure', False)

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `s3:*`, and principal `AWS: *`, without any condition' in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'S3 Bucket')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'S3 Policy')