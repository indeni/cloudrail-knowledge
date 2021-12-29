from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.policy_wildcard_violation_rules import \
    EnsureLambdaFunctionPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLambdaFunctionPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionPolicyNotUseWildcard()

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_action_principal_secure', False)
    def test_not_secure_action_principal_secure(self, rule_result: RuleResponse):
        pass

    @rule_test("secure_policy_from_dome9_tests", False)
    def test_secure_policy_from_dome9_tests(self, rule_result: RuleResponse):
        pass

    @rule_test("not_secure_action_and_principal_condition_secure", False)
    def test_not_secure_action_and_principal_condition_secure(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `lambda:*`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Lambda Function')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Lambda Policy')
