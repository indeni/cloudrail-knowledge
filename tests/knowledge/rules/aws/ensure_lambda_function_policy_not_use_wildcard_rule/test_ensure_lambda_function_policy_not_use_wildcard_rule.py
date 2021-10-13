from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureLambdaFunctionPolicyNotUseWildcard
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLambdaFunctionPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionPolicyNotUseWildcard()

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_action_principal_secure(self):
        self.run_test_case('not_secure_action_principal_secure', False)

    def test_secure_policy_from_dome9_tests(self):
        self.run_test_case("secure_policy_from_dome9_tests", False)

    def test_not_secure_action_and_principal_condition_secure(self):
        self.run_test_case("not_secure_action_and_principal_condition_secure", False)

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `lambda:*`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Lambda Function')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Lambda Policy')
