from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_log_validation_enabled_rule import \
    EnsureCloudTrailLogValidationEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test

class TestEnsureCloudTrailLogValidationEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudTrailLogValidationEnabledRule()

    @rule_test('file_log_validation_disabled', True)
    def test_file_log_validation_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('file_log_validation_enabled', False)
    def test_file_log_validation_enabled(self, rule_result: RuleResponse):
        pass
