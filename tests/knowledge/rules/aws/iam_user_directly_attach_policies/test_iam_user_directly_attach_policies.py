from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.iam_user_directly_attach_policies_rule import IAMUserDirectlyAttachPoliciesRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIamUserDirectlyAttachPolicies(AwsBaseRuleTest):

    def get_rule(self):
        return IAMUserDirectlyAttachPoliciesRule()

    @rule_test('iam_user_inline_policy_attach', True)
    def test_iam_user_inline_policy_attach(self, rule_result: RuleResponse):
        pass

    @rule_test('iam_user_managed_policy_attach', True)
    def test_iam_user_managed_policy_attach(self, rule_result: RuleResponse):
        pass

    @rule_test('iam_user_in_direct_policy_attachment', False)
    def test_iam_user_in_direct_policy_attachment(self, rule_result: RuleResponse):
        pass
