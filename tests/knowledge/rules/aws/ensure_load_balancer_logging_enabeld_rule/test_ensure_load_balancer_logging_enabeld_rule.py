from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_load_balancer_logging_enabeld_rule import \
    EnsureLoadBalancerLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLoadBalancerLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerLoggingEnabledRule()

    def test_access_logging_disabled(self):
        self.run_test_case('access_logging_disabled', True)

    def test_access_logging_disabled_no_block(self):
        self.run_test_case('access_logging_disabled_no_block', True)

    def test_access_logging_enabled(self):
        self.run_test_case('access_logging_enabled', False)
