from cloudrail.knowledge.rules.aws.non_context_aware.iam_account_pass_policy.iam_account_pass_policy_rules import EnsureIamPasswordRequiresNumber
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureIamPasswordRequiresNumber(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureIamPasswordRequiresNumber()

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_policy(self):
        self.run_test_case('not_secure_policy', True)

    def test_not_secure_missing_param(self):
        self.run_test_case('not_secure_missing_param', True)
