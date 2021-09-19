from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_xray_tracing_enabled_rule import \
    EnsureLambdaFunctionXrayTracingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLambdaFunctionXrayTracingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLambdaFunctionXrayTracingEnabledRule()

    def test_xray_disabled(self):
        self.run_test_case('xray_disabled', True)

    def test_xray_enabled(self):
        self.run_test_case('xray_enabled', False)
