from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureSqsQueuePolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSqsQueuePolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSqsQueuePolicyNotUseWildcard()

    @rule_test('bad_policy', True)
    def test_bad_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'SQS queue')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'SQS queue resource policy')

    @rule_test('good_policy', False)
    def test_good_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('secure_policy_existing_queue', False)
    def test_secure_policy_existing_queue(self, rule_result: RuleResponse):
        pass

    @rule_test('non_secure_policy_existing_queue', True)
    def test_non_secure_policy_existing_queue(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'SQS queue')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'SQS queue resource policy')
