from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_load_balancer_logging_enabeld_rule import \
    EnsureLoadBalancerLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLoadBalancerLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerLoggingEnabledRule()

    @rule_test('access_logging_disabled', True)
    def test_access_logging_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('access_logging_disabled_no_block', True)
    def test_access_logging_disabled_no_block(self, rule_result: RuleResponse):
        pass

    @rule_test('access_logging_enabled', False)
    def test_access_logging_enabled(self, rule_result: RuleResponse):
        pass
