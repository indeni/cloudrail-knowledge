from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_warning_and_suggestion_rule import \
    AccessAnalyzerValidationWarningAndSuggestionRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestAccessAnalyzerValidationWarningAndSuggestionBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return AccessAnalyzerValidationWarningAndSuggestionRule()

    def test_kms_key_secure_policy_missing_principal(self):
        self.run_test_case('kms_key_secure_policy_missing_principal', False)

    def test_iam_multiple_issues(self):
        self.run_test_case('iam_multiple_issues', True, number_of_issue_items=1)

    def test_iam_security_issues(self):
        self.run_test_case('iam_security_issues', True, number_of_issue_items=1)
