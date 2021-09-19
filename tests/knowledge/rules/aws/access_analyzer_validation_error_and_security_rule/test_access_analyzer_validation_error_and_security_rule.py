from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_error_and_security_rule import \
    AccessAnalyzerValidationErrorAndSecurityRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestAccessAnalyzerValidationErrorAndSecurityRule(AwsBaseRuleTest):

    def get_rule(self):
        return AccessAnalyzerValidationErrorAndSecurityRule()

    def test_iam_user_inline_policy_attach(self):
        self.run_test_case('iam_user_inline_policy_attach', False)

    def test_iam_user_managed_policy_attach(self):
        self.run_test_case('iam_user_managed_policy_attach', False)

    def test_kms_key_secure_policy(self):
        self.run_test_case('kms_key_secure_policy_valid', False)

    def test_kms_key_secure_policy_missing_principal(self):
        self.run_test_case('kms_key_secure_policy_missing_principal', True, number_of_issue_items=1)

    def test_iam_multiple_issues(self):
        rule_result = self.run_test_case('iam_multiple_issues', True, number_of_issue_items=2)
        for issue_item in rule_result.issues:
            if issue_item.exposed.iac_state.address == 'aws_iam_role_policy.allow-policy-1':
                self.assertIn('The action \'iam: passrole\' does not exist', issue_item.evidence)
            elif issue_item.exposed.iac_state.address == 'aws_iam_role_policy.allow-policy-2':
                self.assertIn('The action \'lambda: createfunction\' does not exist', issue_item.evidence)
                self.assertIn('The action \'lambda: invokefunc*\' does not exist', issue_item.evidence)
            else:
                self.fail(f'issue item id {issue_item.exposed.iac_state.address} is unknown')

    def test_iam_security_issues(self):
        rule_result = self.run_test_case('iam_security_issues', True, number_of_issue_items=1)
        evidence = rule_result.issues[0].evidence
        self.assertIn('Using the iam:PassRole action with wildcards (*) in the resource can be overly permissive', evidence)
