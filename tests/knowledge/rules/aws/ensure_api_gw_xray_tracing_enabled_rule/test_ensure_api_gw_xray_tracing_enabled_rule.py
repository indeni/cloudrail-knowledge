from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_api_gw_xray_tracing_enabled_rule import \
    EnsureApiGwXrayTracingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureApiGwXrayTracingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwXrayTracingEnabledRule()

    def test_api_stage_xray_trace_disable(self):
        self.run_test_case('api_stage_xray_trace_disable', True)

    def test_api_stage_xray_trace_enable(self):
        self.run_test_case('api_stage_xray_trace_enable', False)

    def test_api_without_stage(self):
        self.run_test_case('api_without_stage', False)
