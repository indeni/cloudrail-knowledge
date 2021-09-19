from cloudrail.knowledge.rules.azure.non_context_aware.function_app_client_certificate_mode_rule import FunctionAppClientCertificateModeRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppClientCert(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppClientCertificateModeRule()

    def test_client_cert_required(self):
        self.run_test_case('client_cert_required',
                           should_alert=False)

    def test_client_cert_optional(self):
        self.run_test_case('client_cert_optional',
                           should_alert=True)
