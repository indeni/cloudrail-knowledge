from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_read_only_access_policy_used_by_role_user_rule import \
    EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule


class TestEnsureNoReadOnlyAccessPolicyUsedByRoleUserRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule()

    def test_iam_read_only_policy_role(self):
        rule_result = self.run_test_case('iam_read_only_policy_role', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM Role `aws_iam_role.role` is assigned ReadOnlyAccess policy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM Role')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM Role')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role.role')

    def test_iam_read_only_policy_user(self):
        rule_result = self.run_test_case('iam_read_only_policy_user', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM user `aws_iam_user.console_user` is assigned ReadOnlyAccess policy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM user')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM user')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_user.console_user')

    def test_no_violation_role_user(self):
        self.run_test_case('no_violation_role_user', False)

    def test_iam_group_read_only_policy(self):
        self.run_test_case('iam_group_read_only_policy', False)

    def test_iam_group_console_user_read_only_policy(self):
        rule_result = self.run_test_case('iam_group_console_user_read_only_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('The IAM user `aws_iam_user.group_user` inherit ReadOnlyAccess policy, via group(s)' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'IAM Group')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'IAM Group')
