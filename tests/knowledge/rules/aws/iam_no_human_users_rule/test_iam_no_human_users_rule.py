from cloudrail.knowledge.rules.aws.non_context_aware.iam_no_human_users_rule import IamNoHumanUsersRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestIamNoHumanUsersRule(AwsBaseRuleTest):

    def get_rule(self):
        return IamNoHumanUsersRule()

    def test_login_user(self):
        self.run_test_case('login_user', True)

    def test_no_login_users(self):
        self.run_test_case('no_login_users', False)
