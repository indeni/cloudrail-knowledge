from typing import List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.resources.iam.role import Role

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestIamRole(AwsContextTest):

    def get_component(self):
        return "iam/iam_role"

    @context(module_path="assume-role-inline-policy")
    def test_assume_role_policy(self, ctx: AwsEnvironmentContext):
        role = next((role for role in ctx.roles if role.role_name == 'ec2-assume-role'), None)
        self.assertIsNotNone(role)
        self.assertEqual(role.assume_role_policy.statements[0].principal.principal_values[0], 'ec2.amazonaws.com')
        self.assertEqual(role.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/iam/home?region=us-east-1#/roles/ec2-assume-role')

    @context(module_path="role-inline-policy")
    def test_role_inline_policy(self, ctx: AwsEnvironmentContext):
        self._assert_role_inline_policy(ctx)

    @context(module_path="role-attached-policy")
    def test_role_attached_policy(self, ctx: AwsEnvironmentContext):
        self._assert_policy(ctx=ctx, role_name="s3-role", policy_name="s3-policy",
                            actions=["s3:*"], resources=["arn:aws:s3:::*"],
                            principals=[], principals_type=PrincipalType.NO_PRINCIPAL)

    @context(module_path="role-with-permission-boundary")
    def test_role_with_permission_boundary(self, ctx: AwsEnvironmentContext):
        permission_boundary_policy = next((policy for policy in ctx.policies if policy.policy_name == 'permission_boundary_policy'), None)
        self.assertTrue(permission_boundary_policy)
        role = next((role for role in ctx.roles if role.role_name == 'ec2-role'), None)
        self.assertTrue(role)
        self.assertEqual(role.permission_boundary, permission_boundary_policy)

    def _assert_policy(self, ctx: AwsEnvironmentContext, role_name: str,
                       policy_name: str,
                       actions: List[str], resources: List[str],
                       principals: List[str], principals_type: PrincipalType):
        self.assertEqual(len(ctx.roles), 1)
        role: Role = ctx.roles[0]
        self.assertEqual(role.role_name, role_name)
        self.assertGreater(len(role.permissions_policies), 0)

        policy: Policy = next(iter(policy for policy in role.permissions_policies if policy.policy_name == policy_name), None)
        self.assertIsNotNone(policy)
        self.assertEqual(len(policy.statements), 1)
        statement: PolicyStatement = policy.statements[0]
        self.assertEqual(statement.actions, actions)
        self.assertEqual(statement.effect, StatementEffect.ALLOW)
        self.assertEqual(statement.principal.principal_values, principals)
        self.assertEqual(statement.principal.principal_type, principals_type)
        self.assertEqual(statement.resources, resources)

    @context(module_path="role_with_tags")
    def test_role_with_tags(self, ctx: AwsEnvironmentContext):
        role = next((role for role in ctx.roles if role.role_name == 'ec2-role'), None)
        self.assertIsNotNone(role)
        self.assertTrue(role.tags)

    @context(module_path="role-nested-inline-policy")
    def test_role_nested_inline_policy(self, ctx: AwsEnvironmentContext):
        self._assert_role_inline_policy(ctx)

    def _assert_role_inline_policy(self, ctx: AwsEnvironmentContext):
        self._assert_policy(ctx=ctx, role_name="ec2-role", policy_name="ec2-describe-policy",
                            actions=["ec2:Describe*"], resources=["*"],
                            principals=[], principals_type=PrincipalType.NO_PRINCIPAL)
        role = next((role for role in ctx.roles if role.role_name == 'ec2-role'), None)
        self.assertIsNotNone(role)
        self.assertFalse(role.tags)

    @context(module_path="testing_dates", base_scanner_data_for_iac='account-data-iam-role-last-used',
             test_options=TestOptions(use_state_file=True))
    def test_testing_dates(self, ctx: AwsEnvironmentContext):
        role = next((role for role in ctx.roles if role.role_name == 'dates-test-role'), None)
        self.assertIsNotNone(role)
        self.assertTrue(role.creation_date)
        self.assertTrue(role.last_used_date)

    @context(module_path="two-roles-same-policy")
    def test_two_roles_same_policy(self, ctx: AwsEnvironmentContext):
        role = [role for role in ctx.roles if any(policy.policy_name == 'ec2-describe-policy' for policy in role.permissions_policies)]
        self.assertIsNotNone(role)
        self.assertTrue(len(role), 2)
