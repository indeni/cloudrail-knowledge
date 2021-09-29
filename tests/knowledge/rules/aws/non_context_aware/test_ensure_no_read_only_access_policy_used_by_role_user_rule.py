import unittest

from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.resources.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, ManagedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_read_only_access_policy_used_by_role_user_rule import \
    EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureNoReadOnlyAccessPolicyUsedByRoleUserRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule()

    def test_non_car_iam_readonlyaccess_policy__user_attached__fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        user: IamUser = create_empty_entity(IamUser)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        account.account = '111111111'
        user_login_profile.name = 'user_login_profile'
        user.account = '111111111'
        user.name = 'user_login_profile'
        user.permissions_policies = [managed_policy]
        context = AwsEnvironmentContext(accounts=[account], users=[user], users_login_profile=[user_login_profile])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is assigned ReadOnlyAccess policy" in result.issues[0].evidence)

    def test_non_car_iam_readonlyaccess_policy__user_inherit_from_group__fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        user: IamUser = create_empty_entity(IamUser)
        group: IamGroup = create_empty_entity(IamGroup)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        account.account = '111111111'
        user_login_profile.name = 'user_login_profile'
        group.account = '111111111'
        group.permissions_policies = [managed_policy]
        group.name = 'violating_group'
        user.account = '111111111'
        user.name = 'user_login_profile'
        user.groups = [group]
        context = AwsEnvironmentContext(accounts=[account],
                                        users=[user],
                                        groups=[group],
                                        users_login_profile=[user_login_profile],
                                        policies=[managed_policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("inherit ReadOnlyAccess policy" in result.issues[0].evidence)

    def test_non_car_iam_readonlyaccess_policy__role_attached__fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.PUBLIC, ['*']))], 'state_id')
        assume_role_policy.is_allowing_external_assume = True
        account.account = '111111111'
        role.account = '111111111'
        role.name = 'user_login_profile'
        role.permissions_policies = [managed_policy]
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is assigned ReadOnlyAccess policy" in result.issues[0].evidence)

    def test_non_car_iam_readonlyaccess_policy__role_secure_assume_policy__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.PUBLIC, ['*.amazonaws.com']))], 'state_id')
        account.account = '111111111'
        role.account = '111111111'
        role.name = 'user_login_profile'
        role.permissions_policies = [managed_policy]
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_iam_readonlyaccess_policy__role_not_readonly_policy__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'not_readonly',
                                       'arn:aws:iam::aws:policy/not_readonly',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.PUBLIC, ['*']))], 'state_id')
        account.account = '111111111'
        role.account = '111111111'
        role.name = 'user_login_profile'
        role.permissions_policies = [managed_policy]
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_iam_readonlyaccess_policy__user_not_login__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        user: IamUser = create_empty_entity(IamUser)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        account.account = '111111111'
        user_login_profile.name = 'user_login_profile'
        user.account = '111111111'
        user.name = 'user_not_login_profile'
        user.permissions_policies = [managed_policy]
        context = AwsEnvironmentContext(accounts=[account], users=[user], users_login_profile=[user_login_profile])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_iam_readonlyaccess_policy__user_secure_policy__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        user: IamUser = create_empty_entity(IamUser)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'not_readonly',
                                       'arn:aws:iam::aws:policy/not_readonly',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        account.account = '111111111'
        user_login_profile.name = 'user_login_profile'
        user.account = '111111111'
        user.name = 'user_login_profile'
        user.permissions_policies = [managed_policy]
        context = AwsEnvironmentContext(accounts=[account], users=[user], users_login_profile=[user_login_profile])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
