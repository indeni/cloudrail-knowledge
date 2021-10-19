from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_global_acceleration_flow_logs_enabled_rule import \
    EnsureGlobalAccelerationFlowLogsEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureGlobalAccelerationFlowLogsEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureGlobalAccelerationFlowLogsEnabledRule()

    @rule_test('flow_logs_disabled', True)
    def test_flow_logs_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('flow_logs_disabled_no_attributes', True)
    def test_flow_logs_disabled_no_attributes(self, rule_result: RuleResponse):
        pass

    @rule_test('flow_logs_enabled', False)
    def test_flow_logs_enabled(self, rule_result: RuleResponse):
        pass
