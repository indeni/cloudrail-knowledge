from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.policy_wildcard_violation_rules import \
    EnsureCloudWatchLogDestinationPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudWatchLogDestinationPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogDestinationPolicyNotUseWildcard()

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_actions_secure_principal', True)
    def test_not_secure_actions_secure_principal(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using wildcard action `logs:*`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using wildcard action `logs:*`, and principal `AWS: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('secure_action_not_secure_principal', True)
    def test_secure_action_not_secure_principal(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `AWS: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('multiple_statements_scenario', True)
    def test_multiple_statements_scenario(self, rule_result: RuleResponse):  # the rule evaluate 2 scenarios, but it's being filtered by base_rule.py
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('no_policy_at_all', True)
    def test_no_policy_at_all(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("There is no resource policy or no statements attached to "
                        "`aws_cloudwatch_log_destination.test_destination`" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination')

    @rule_test('federated_principal_violating', True)
    def test_federated_principal_violating(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `Federated: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('service_principal_violating', True)
    def test_service_principal_violating(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `Service: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    @rule_test('canonicaluser_principal_violating', True)
    def test_canonicaluser_principal_violating(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `CanonicalUser: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')
