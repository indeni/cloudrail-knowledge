from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.policy import InlinePolicy, ManagedPolicy
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.exceptions import UnknownResultOfTerraformApply

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestIamPolicyAttachment(AwsContextTest):

    def get_component(self):
        return "iam"

    @context(module_path="iam_policy_attachment", test_options=TestOptions(run_cloudmapper=False))
    def test_iam_policy_attachment(self, ctx: AwsEnvironmentContext):
        policy_attachment = next((attachment for attachment in ctx.iam_policy_attachments
                                  if attachment.attachment_name == 'test-attachment'), None)
        self.assertIsNotNone(policy_attachment)
        self.assertTrue(policy_attachment.groups)
        self.assertTrue(policy_attachment.roles)
        self.assertTrue(policy_attachment.users)
        self.assertEqual(policy_attachment.policy_arn, 'arn:aws:iam::aws:policy/ReadOnlyAccess')
        self.assertEqual(policy_attachment.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/iam/home?region=us-east-1#/policies')

    @context(module_path="iam_policy_attachment", base_scanner_data_for_iac='account-data-read-only-policy', test_options=TestOptions(run_cloudmapper=False))
    def test_assigner_for_user_role_group(self, ctx: AwsEnvironmentContext):
        self.assertTrue(any(self._is_policy(user) for user in ctx.users))
        self.assertTrue(any(self._is_policy(group) for group in ctx.groups))
        self.assertTrue(any(self._is_policy(role) for role in ctx.roles))

    @staticmethod
    def _is_policy(resource: IamIdentity) -> bool:
        for item in resource.permissions_policies:
            if isinstance(item, (ManagedPolicy, InlinePolicy)):
                return item.policy_name == 'ReadOnlyAccess'
            else:
                return False

    @context(module_path="iam_policy_attachment_raise_exception",
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False, expected_exception=UnknownResultOfTerraformApply))
    def test_iam_policy_attachment_raise_exception(self, ctx: AwsEnvironmentContext):
        pass
