from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rest_api_gw_access_logging_enabled_rule import \
    EnsureRestApiGwAccessLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureRestApiGwAccessLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRestApiGwAccessLoggingEnabledRule()

    @rule_test('logging_enabled', False)
    def test_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_disabled', True)
    def test_logging_disabled(self, rule_result: RuleResponse):
        pass
