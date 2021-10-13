from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_global_acceleration_flow_logs_enabled_rule import \
    EnsureGlobalAccelerationFlowLogsEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureGlobalAccelerationFlowLogsEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureGlobalAccelerationFlowLogsEnabledRule()

    def test_flow_logs_disabled(self):
        self.run_test_case('flow_logs_disabled', True)

    def test_flow_logs_disabled_no_attributes(self):
        self.run_test_case('flow_logs_disabled_no_attributes', True)

    def test_flow_logs_enabled(self):
        self.run_test_case('flow_logs_enabled', False)
