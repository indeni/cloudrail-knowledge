from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_client_certificate_mode_rule import FunctionAppClientCertificateModeRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppClientCert(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppClientCertificateModeRule()

    @rule_test('client_cert_required', should_alert=False)
    def test_client_cert_required(self, rule_result: RuleResponse):
        pass

    @rule_test('client_cert_optional', should_alert=True)
    def test_client_cert_optional(self, rule_result: RuleResponse):
        pass
