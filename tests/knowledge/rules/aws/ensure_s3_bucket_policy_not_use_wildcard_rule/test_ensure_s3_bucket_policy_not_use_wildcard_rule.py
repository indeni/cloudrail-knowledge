from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureS3BucketPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureS3BucketPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketPolicyNotUseWildcard()

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_action_principal_and_condition_secure', False)
    def test_not_secure_action_principal_and_condition_secure(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `s3:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'S3 Bucket')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'S3 Policy')
