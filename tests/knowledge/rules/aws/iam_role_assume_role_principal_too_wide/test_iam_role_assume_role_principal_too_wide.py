from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.iam_role_assume_role_principal_too_wide import IamRoleAssumeRolePrincipalTooWide
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestIamRoleAssumeRolePrincipalTooWide(AwsBaseRuleTest):

    def get_rule(self):
        return IamRoleAssumeRolePrincipalTooWide()

    @rule_test('assume-role-all-auth-users-principals', True)
    def test_assume_role_all_auth_users_principals(self, rule_result: RuleResponse):
        pass

    @rule_test('assume-role-public-principals', True)
    def test_assume_role_public_principals(self, rule_result: RuleResponse):
        pass

    @rule_test('assume-role-restricted-principals', False)
    def test_assume_role_restricted_principal(self, rule_result: RuleResponse):
        pass
