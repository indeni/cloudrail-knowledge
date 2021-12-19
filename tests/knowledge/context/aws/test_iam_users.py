from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestIamUsers(AwsContextTest):

    def get_component(self):
        return "iam/iam_users"

    @context(module_path="login_user")
    def test_login_user(self, ctx: AwsEnvironmentContext):
        self.assertTrue(any(user.server_name == 'iam_user_1' for user in ctx.users_login_profile))

    @context(module_path="user-with-permission-boundary")
    def test_user_with_permission_boundary(self, ctx: AwsEnvironmentContext):
        permission_boundary_policy = next((policy for policy in ctx.policies if policy.policy_name == 'permission_boundary_policy'), None)
        self.assertTrue(permission_boundary_policy)
        user = next((user for user in ctx.users if user.server_name == 'test-user'), None)
        self.assertTrue(user)
        self.assertEqual(user.permission_boundary, permission_boundary_policy)
        self.assertFalse(user.tags)
        self.assertEqual(user.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/iam/home?region=us-east-1#/users/test-user')

    @context(module_path="user_with_tags")
    def test_user_with_tags(self, ctx: AwsEnvironmentContext):
        user = next((user for user in ctx.users if user.server_name == 'iam_user_1'), None)
        self.assertTrue(user.tags)
