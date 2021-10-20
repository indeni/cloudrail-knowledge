from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_api_gw_xray_tracing_enabled_rule import \
    EnsureApiGwXrayTracingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureApiGwXrayTracingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwXrayTracingEnabledRule()

    @rule_test('api_stage_xray_trace_disable', True)
    def test_api_stage_xray_trace_disable(self, rule_result: RuleResponse):
        pass

    @rule_test('api_stage_xray_trace_enable', False)
    def test_api_stage_xray_trace_enable(self, rule_result: RuleResponse):
        pass

    @rule_test('api_without_stage', False)
    def test_api_without_stage(self, rule_result: RuleResponse):
        pass
