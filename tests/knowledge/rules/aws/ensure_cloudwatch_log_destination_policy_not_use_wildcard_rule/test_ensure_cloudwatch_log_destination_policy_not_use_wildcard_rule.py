from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureCloudWatchLogDestinationPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudWatchLogDestinationPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudWatchLogDestinationPolicyNotUseWildcard()

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_actions_secure_principal(self):
        rule_result = self.run_test_case('not_secure_actions_secure_principal', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using wildcard action `logs:*`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using wildcard action `logs:*`, and principal `AWS: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_secure_action_not_secure_principal(self):
        rule_result = self.run_test_case('secure_action_not_secure_principal', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `AWS: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_multiple_statements_scenario(self):  # the rule evaluate 2 scenarios, but it's being filtered by base_rule.py
        rule_result = self.run_test_case('multiple_statements_scenario', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_no_policy_at_all(self):
        rule_result = self.run_test_case('no_policy_at_all', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("There is no resource policy or no statements attached to "
                        "`aws_cloudwatch_log_destination.test_destination`" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination')

    def test_federated_principal_violating(self):
        rule_result = self.run_test_case('federated_principal_violating', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `Federated: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_service_principal_violating(self):
        rule_result = self.run_test_case('service_principal_violating', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `Service: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')

    def test_canonicaluser_principal_violating(self):
        rule_result = self.run_test_case('canonicaluser_principal_violating', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("the CloudWatch Logs Destination `aws_cloudwatch_log_destination.test_destination`"
                        " is using principal `CanonicalUser: *`, without any condition" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudWatch Logs Destination')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudWatch Logs Destination policy')
