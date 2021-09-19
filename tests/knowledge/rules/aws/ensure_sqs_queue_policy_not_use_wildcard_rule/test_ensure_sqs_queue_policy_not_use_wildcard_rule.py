from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureSqsQueuePolicyNotUseWildcard
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSqsQueuePolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSqsQueuePolicyNotUseWildcard()

    def test_bad_policy(self):
        rule_result = self.run_test_case('bad_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'SQS queue')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'SQS queue resource policy')

    def test_good_policy(self):
        self.run_test_case('good_policy', False)

    def test_secure_policy_existing_queue(self):
        self.run_test_case('secure_policy_existing_queue', False)

    def test_non_secure_policy_existing_queue(self):
        rule_result = self.run_test_case('non_secure_policy_existing_queue', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'SQS queue')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'SQS queue resource policy')
