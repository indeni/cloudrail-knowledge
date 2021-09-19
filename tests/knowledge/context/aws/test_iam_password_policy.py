from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestIamPasswordPolicy(AwsContextTest):

    def get_component(self):
        return "iam/iam_account_policy"

    @context(module_path="password_expiriation")
    def test_password_expiriation(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.iam_account_pass_policies), 1)
        account_policy = next((policy for policy in ctx.iam_account_pass_policies
                               if policy.account == '111111111111'), None)
        self.assertIsNotNone(account_policy)
        self.assertIsInstance(account_policy.min_pass_length, int)
        self.assertIsInstance(account_policy.max_pass_age, int)
        self.assertTrue(account_policy.require_low_case_characters)
        self.assertTrue(account_policy.require_numbers)
        self.assertTrue(account_policy.require_upper_case_characters)
        self.assertTrue(account_policy.require_symbols)
        self.assertTrue(account_policy.allow_users_to_change_pass)
        self.assertEqual(account_policy.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/iam/home?region=us-east-1#/account_settings$editPasswordPolicy?step=passwordPolicy')

    @context(module_path="some_missing_config")
    def test_some_missing_config(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.iam_account_pass_policies), 1)
        account_policy = next((policy for policy in ctx.iam_account_pass_policies
                               if policy.account == '111111111111'), None)
        self.assertIsNotNone(account_policy)
        self.assertIsInstance(account_policy.min_pass_length, int)
        self.assertFalse(account_policy.max_pass_age)
        self.assertTrue(account_policy.require_low_case_characters)
        self.assertTrue(account_policy.require_numbers)
        self.assertTrue(account_policy.require_upper_case_characters)
        self.assertTrue(account_policy.require_symbols)
        self.assertTrue(account_policy.allow_users_to_change_pass)

    @context(module_path="password_reuse")
    def test_password_reuse(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.iam_account_pass_policies), 1)
        account_policy = next((policy for policy in ctx.iam_account_pass_policies
                               if policy.account == '111111111111'), None)
        self.assertIsNotNone(account_policy)
        self.assertIsInstance(account_policy.min_pass_length, int)
        self.assertIsInstance(account_policy.max_pass_age, int)
        self.assertIsInstance(account_policy.password_reuse_prevention, int)
        self.assertTrue(account_policy.require_low_case_characters)
        self.assertTrue(account_policy.require_numbers)
        self.assertTrue(account_policy.require_upper_case_characters)
        self.assertTrue(account_policy.require_symbols)
        self.assertTrue(account_policy.allow_users_to_change_pass)
