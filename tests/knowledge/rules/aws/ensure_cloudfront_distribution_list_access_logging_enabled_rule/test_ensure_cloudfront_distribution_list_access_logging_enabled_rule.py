from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudfront_distribution_list_access_logging_enabled_rule import \
    EnsureCloudfrontDistributionListAccessLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudfrontDistributionListAccessLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudfrontDistributionListAccessLoggingEnabledRule()

    @rule_test('logging_enabled_basic_config', False)
    def test_logging_enabled_basic_config(self, rule_result: RuleResponse):
        pass

    @rule_test('no_logging_at_all', True)
    def test_no_logging_at_all(self, rule_result: RuleResponse):
        pass

    @rule_test('with_logging_access_enabled', False)
    def test_with_logging_access_enabled(self, rule_result: RuleResponse):
        pass
