from cloudrail.knowledge.rules.aws.non_context_aware.iam_role_assume_role_principal_too_wide import IamRoleAssumeRolePrincipalTooWide
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestIamRoleAssumeRolePrincipalTooWide(AwsBaseRuleTest):

    def get_rule(self):
        return IamRoleAssumeRolePrincipalTooWide()

    def test_assume_role_all_auth_users_principals(self):
        self.run_test_case('assume-role-all-auth-users-principals', True)

    def test_assume_role_public_principals(self):
        self.run_test_case('assume-role-public-principals', True)

    def test_assume_role_restricted_principal(self):
        self.run_test_case('assume-role-restricted-principals', False)
