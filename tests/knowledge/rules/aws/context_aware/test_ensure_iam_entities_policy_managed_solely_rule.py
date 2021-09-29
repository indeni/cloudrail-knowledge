import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy import ManagedPolicy, InlinePolicy
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.mergeable import EntityOrigin
from cloudrail.knowledge.rules.aws.context_aware.ensure_iam_entities_policy_managed_solely_rule import EnsureIamEntitiesPolicyManagedSolely
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity, add_terraform_state


class TestEnsureIamEntitiesPolicyManagedSolely(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamEntitiesPolicyManagedSolely()

    def test_car_iam_policy_control_in_iac_only_fail(self):
        # Arrange
        account = create_empty_entity(Account)
        role = create_empty_entity(Role)
        add_terraform_state(role, 'role', False)
        account.account = role.account = '123456789012'

        managed_policy = create_empty_entity(ManagedPolicy, statements=[])
        managed_policy.policy_name = 'managed_policy_name'

        inline_policy = create_empty_entity(InlinePolicy, statements=[])
        managed_policy.policy_name = 'inline_policy_name'
        add_terraform_state(inline_policy, 'inline_policy')

        role.policy_attach_origin_map = [{managed_policy.policy_name: EntityOrigin.LIVE_ENV},
                                         {inline_policy.policy_name: EntityOrigin.TERRAFORM}]
        role.permissions_policies.append(managed_policy)
        role.permissions_policies.append(inline_policy)

        context = AwsEnvironmentContext(accounts=AliasesDict(account),
                                        roles=[role],
                                        policies=[managed_policy, inline_policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_car_iam_policy_control_in_iac_only_pass_policies_attached_by_terraform(self):
        # Arrange
        account = create_empty_entity(Account)
        role = create_empty_entity(Role)
        add_terraform_state(role, 'role', False)
        account.account = role.account = '123456789012'

        managed_policy = create_empty_entity(ManagedPolicy, statements=[])
        managed_policy.policy_name = 'managed_policy_name'

        inline_policy = create_empty_entity(InlinePolicy, statements=[])
        managed_policy.policy_name = 'inline_policy_name'
        add_terraform_state(inline_policy, 'inline_policy')

        role.policy_attach_origin_map = [{managed_policy.policy_name: EntityOrigin.TERRAFORM},
                                         {inline_policy.policy_name: EntityOrigin.TERRAFORM}]
        role.permissions_policies.append(managed_policy)
        role.permissions_policies.append(inline_policy)

        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
