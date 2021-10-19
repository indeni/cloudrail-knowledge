from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.iam_no_human_users_rule import IamNoHumanUsersRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIamNoHumanUsersRule(AwsBaseRuleTest):

    def get_rule(self):
        return IamNoHumanUsersRule()

    @rule_test('login_user', True)
    def test_login_user(self, rule_result: RuleResponse):
        pass

    @rule_test('no_login_users', False)
    def test_no_login_users(self, rule_result: RuleResponse):
        pass
