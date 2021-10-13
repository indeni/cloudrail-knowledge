from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rds_resource_logging_enabled_rule import \
    EnsureRdsResourceLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRdsResourceLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsResourceLoggingEnabledRule()

    def test_logging_disabled(self):
        self.run_test_case('logging_disabled', True, 2)

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)
