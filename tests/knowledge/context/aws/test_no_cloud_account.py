from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from test.knowledge.context.aws_context_test import AwsNoCloudAccountContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestNoCloudAccount(AwsNoCloudAccountContextTest):

    def get_component(self):
        return 'no_cloud_account'

    @context(module_path="role", test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_role_no_cloud_account(self, ctx: AwsEnvironmentContext):
        role = next((role for role in ctx.roles if role.role_name == 'test-role-name'), None)
        self.assertIsNotNone(role)
        self.assertEqual(role.account, '000000000000')
