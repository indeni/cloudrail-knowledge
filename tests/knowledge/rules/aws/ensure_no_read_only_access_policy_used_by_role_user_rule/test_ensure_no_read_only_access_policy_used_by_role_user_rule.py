from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_read_only_access_policy_used_by_role_user_rule import \
    EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule


class TestEnsureNoReadOnlyAccessPolicyUsedByRoleUserRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule()

    @rule_test('iam_read_only_policy_role', True)
    def test_iam_read_only_policy_role(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM Role `aws_iam_role.role` is assigned ReadOnlyAccess policy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM Role')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM Role')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role.role')

    @rule_test('iam_read_only_policy_user', True)
    def test_iam_read_only_policy_user(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM user `aws_iam_user.console_user` is assigned ReadOnlyAccess policy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM user')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM user')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_user.console_user')

    @rule_test('no_violation_role_user', False)
    def test_no_violation_role_user(self, rule_result: RuleResponse):
        pass

    @rule_test('iam_group_read_only_policy', False)
    def test_iam_group_read_only_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('iam_group_console_user_read_only_policy', True)
    def test_iam_group_console_user_read_only_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM user `aws_iam_user.group_user` inherit ReadOnlyAccess policy, via group(s)' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM Group')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM Group')
