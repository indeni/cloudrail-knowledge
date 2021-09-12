import unittest
from datetime import datetime, timedelta

from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_unused_roles_removed_rule import EnsureUnusedRolesRemoved
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIamNoHumanUsersRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureUnusedRolesRemoved()

    def test_non_car_unused_roles__old_role_not_used_lately__fail(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        last_used_date: RoleLastUsed = create_empty_entity(RoleLastUsed)
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date - timedelta(days=100), '%Y-%m-%d')
        last_used_date.last_used_date = datetime.strftime(current_date - timedelta(days=90), '%Y-%m-%d')
        role.last_used_date = last_used_date
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.NO_OP,
                                  resource_metadata=None,
                                  is_new=False)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unused_roles__old_role_not_used_at_all__fail(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date - timedelta(days=100), '%Y-%m-%d')
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.NO_OP,
                                  resource_metadata=None,
                                  is_new=False)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unused_roles__lately_used__pass(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        last_used_date: RoleLastUsed = create_empty_entity(RoleLastUsed)
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date - timedelta(days=100), '%Y-%m-%d')
        last_used_date.last_used_date = datetime.strftime(current_date - timedelta(days=10), '%Y-%m-%d')
        role.last_used_date = last_used_date
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.NO_OP,
                                  resource_metadata=None,
                                  is_new=False)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_roles__new_role_never_used__pass(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date, '%Y-%m-%d')
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.NO_OP,
                                  resource_metadata=None,
                                  is_new=False)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_roles__old_role_lately_used__pass(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        last_used_date: RoleLastUsed = create_empty_entity(RoleLastUsed)
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date - timedelta(days=100), '%Y-%m-%d')
        last_used_date.last_used_date = datetime.strftime(current_date, '%Y-%m-%d')
        role.last_used_date = last_used_date
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.NO_OP,
                                  resource_metadata=None,
                                  is_new=False)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_roles__new_role_creating__pass(self):
        # Arrange
        role: Role = create_empty_entity(Role)
        account: Account = create_empty_entity(Account)
        account.account = 'account_id'
        current_date = datetime.today()
        role.role_id = 'role_id'
        role.creation_date = datetime.strftime(current_date, '%Y-%m-%d')
        role.iac_state = IacState(address='address',
                                  action=TerraformActionType.CREATE,
                                  resource_metadata=None,
                                  is_new=True)
        context = AwsEnvironmentContext(roles=[role], accounts=[account])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
