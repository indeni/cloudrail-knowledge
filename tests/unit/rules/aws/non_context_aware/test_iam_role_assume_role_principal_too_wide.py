import unittest

from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_role_assume_role_principal_too_wide import IamRoleAssumeRolePrincipalTooWide
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIamRoleAssumeRolePrincipalTooWide(unittest.TestCase):
    def setUp(self):
        self.rule = IamRoleAssumeRolePrincipalTooWide()

    def test_non_car_iam_role_assume_role_principal_too_wide__public_principal__fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.PUBLIC, ['*']))], 'state_id')
        account.account = '111111111'
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_iam_role_assume_role_principal_too_wide__aws_principal__fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.AWS, ['*']))], 'state_id')
        account.account = '111111111'
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_iam_role_assume_role_principal_too_wide__safe_aws_principal__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.AWS, ['arn:something:some']))], 'state_id')
        account.account = '111111111'
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_iam_role_assume_role_principal_too_wide__safe_condition_block__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        role: Role = create_empty_entity(Role)
        policy_condition = [StatementCondition(operator='BOOL', key='aws:SecureTransport', values=['false'])]
        assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
                                              [PolicyStatement(StatementEffect.ALLOW,
                                                               ['sts:AssumeRole'],
                                                               ['*'],
                                                               Principal(PrincipalType.PUBLIC, ['*']), 'state_id', policy_condition)], 'state_id')
        account.account = '111111111'
        role.assume_role_policy = assume_role_policy
        context = AwsEnvironmentContext(accounts=[account], roles=[role])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
