from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rest_api_gw_access_logging_enabled_rule import \
    EnsureRestApiGwAccessLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRestApiGwAccessLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRestApiGwAccessLoggingEnabledRule()

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)

    def test_logging_disabled(self):
        self.run_test_case('logging_disabled', True)
