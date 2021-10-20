from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_xray_tracing_enabled_rule import \
    EnsureLambdaFunctionXrayTracingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLambdaFunctionXrayTracingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionXrayTracingEnabledRule()

    @rule_test('xray_disabled', True)
    def test_xray_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('xray_enabled', False)
    def test_xray_enabled(self, rule_result: RuleResponse):
        pass
