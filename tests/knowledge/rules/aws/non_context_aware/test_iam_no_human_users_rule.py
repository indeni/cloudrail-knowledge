import unittest

from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_no_human_users_rule import IamNoHumanUsersRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIamNoHumanUsersRule(unittest.TestCase):
    def setUp(self):
        self.rule = IamNoHumanUsersRule()

    def test_non_car_iam_no_human_users_fail(self):
        # Arrange
        user: IamUser = create_empty_entity(IamUser)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(users=[user], users_login_profile=[user_login_profile])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_iam_no_human_users_pass(self):
        # Arrange
        user: IamUser = create_empty_entity(IamUser)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_not_login_profile'
        context = EnvironmentContext(users=[user], users_login_profile=[user_login_profile])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
