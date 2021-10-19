from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.iam_account_pass_policy.iam_account_pass_policy_rules import EnsureIamPasswordRequiresUpperCase
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test

class TestEnsureIamPasswordRequiresUpperCase(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureIamPasswordRequiresUpperCase()

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_missing_param', True)
    def test_not_secure_missing_param(self, rule_result: RuleResponse):
        pass
