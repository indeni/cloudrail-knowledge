import unittest

from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.policy import ManagedPolicy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_user_directly_attach_policies_rule import IAMUserDirectlyAttachPoliciesRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIAMUserDirectlyAttachPoliciesRule(unittest.TestCase):
    def setUp(self):
        self.rule = IAMUserDirectlyAttachPoliciesRule()

    def test_non_car_iam_no_permissions_directly_to_user_fail(self):
        # Arrange
        user: IamUser = create_empty_entity(IamUser)
        managed_policy = ManagedPolicy('111111111',
                                       'ANPAILL3HVNFSB6DCOWYQ',
                                       'ReadOnlyAccess',
                                       'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                       [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                        ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))], 'state_id')
        user.permissions_policies = [managed_policy]
        context = EnvironmentContext(users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_iam_no_permissions_directly_to_user_pass(self):
        # Arrange
        user: IamUser = create_empty_entity(IamUser)
        context = EnvironmentContext(users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
