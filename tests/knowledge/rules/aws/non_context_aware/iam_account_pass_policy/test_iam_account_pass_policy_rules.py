import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_account_pass_policy.iam_account_pass_policy_rules import EnsureIamPasswordExpiration, \
    EnsureIamPasswordLowerCharacters, EnsureIamPasswordMinimumLength, EnsureIamPasswordNotAllowReuse, EnsureIamPasswordRequiresNumber,\
    EnsureIamPasswordRequiresSymbol, EnsureIamPasswordRequiresUpperCase
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureIamPasswordRequiresUpperCase(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordRequiresUpperCase()

    def test_non_car_aws_iam_password_policy_upper_required_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_upper_case_characters = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_upper_required_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_upper_case_characters = True
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_upper_required__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_upper_case_characters = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordRequiresSymbol(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordRequiresSymbol()

    def test_non_car_aws_iam_password_policy_symbol_required_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_symbols = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_symbol_required_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_symbols = True
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_symbol_required__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_symbols = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordNotAllowReuse(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordNotAllowReuse()

    def test_non_car_aws_iam_password_policy_password_reuse_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.password_reuse_prevention = 12
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_password_reuse_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.password_reuse_prevention = 24
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_password_reuse__not_same_account__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '111111234211'
        iam_pass_policy.password_reuse_prevention = 24
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_password_reuse__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.password_reuse_prevention = 24
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordRequiresNumber(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordRequiresNumber()

    def test_non_car_aws_iam_password_policy_num_required_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_numbers = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_num_required_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_numbers = True
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_num_required__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_numbers = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordLowerCharacters(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordLowerCharacters()

    def test_non_car_aws_iam_password_policy_lower_required_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_low_case_characters = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_lower_required_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_low_case_characters = True
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_lower_required__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.require_low_case_characters = False
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordMinimumLength(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordMinimumLength()

    def test_non_car_aws_iam_password_policy_min_length_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.min_pass_length = 10
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_min_length_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.min_pass_length = 16
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_min_length__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.min_pass_length = 10
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureIamPasswordExpiration(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureIamPasswordExpiration()

    def test_non_car_aws_iam_password_policy_min_length_fail(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.max_pass_age = 95
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_iam_password_policy_min_length_pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.max_pass_age = 85
        user_login_profile.name = 'user_login_profile'
        user.name = 'user_login_profile'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_iam_password_policy_min_length__not_same_user__pass(self):
        # Arrange
        account: Account = create_empty_entity(Account)
        iam_pass_policy: IamPasswordPolicy = create_empty_entity(IamPasswordPolicy)
        user_login_profile: IamUsersLoginProfile = create_empty_entity(IamUsersLoginProfile)
        user: IamUser = create_empty_entity(IamUser)
        account.account = '11111111'
        iam_pass_policy.account = '11111111'
        iam_pass_policy.max_pass_age = 95
        user_login_profile.name = 'user_login_profile'
        user.name = 'some_user'
        context = EnvironmentContext(accounts=[account], iam_account_pass_policies=[iam_pass_policy], users_login_profile=[user_login_profile],
                                     users=[user])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
