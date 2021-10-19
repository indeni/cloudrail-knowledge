from cloudrail.knowledge.rules.base_rule import RuleResponse
from unittest import skip

from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_warning_and_suggestion_rule import \
    AccessAnalyzerValidationWarningAndSuggestionRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestAccessAnalyzerValidationWarningAndSuggestionBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return AccessAnalyzerValidationWarningAndSuggestionRule()

    @skip('skipped until we have access in jenkins for boto access analyzer')
    @rule_test('kms_key_secure_policy_missing_principal', False)
    def test_kms_key_secure_policy_missing_principal(self, rule_result: RuleResponse):
        pass

    @skip('skipped until we have access in jenkins for boto access analyzer')
    @rule_test('iam_multiple_issues', True, number_of_issue_items=1)
    def test_iam_multiple_issues(self, rule_result: RuleResponse):
        pass

    @skip('skipped until we have access in jenkins for boto access analyzer')
    @rule_test('iam_security_issues', True, number_of_issue_items=1)
    def test_iam_security_issues(self, rule_result: RuleResponse):
        pass
