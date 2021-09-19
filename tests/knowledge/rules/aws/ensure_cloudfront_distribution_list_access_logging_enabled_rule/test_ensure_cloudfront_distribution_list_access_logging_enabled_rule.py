from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudfront_distribution_list_access_logging_enabled_rule import \
    EnsureCloudfrontDistributionListAccessLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudfrontDistributionListAccessLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudfrontDistributionListAccessLoggingEnabledRule()

    def test_logging_enabled_basic_config(self):
        self.run_test_case('logging_enabled_basic_config', False)

    def test_no_logging_at_all(self):
        self.run_test_case('no_logging_at_all', True)

    def test_with_logging_access_enabled(self):
        self.run_test_case('with_logging_access_enabled', False)
