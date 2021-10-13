from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_tls_version_rule import FunctionAppUseLatestTlsVersionRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppUseLatestTlsVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseLatestTlsVersionRule()

    def test_functionapp_tls_isnot_latest(self):
        self.run_test_case('functionapp_tls_isnot_latest', True)

    def test_functionapp_tls_latest(self):
        self.run_test_case('functionapp_tls_latest', False)
