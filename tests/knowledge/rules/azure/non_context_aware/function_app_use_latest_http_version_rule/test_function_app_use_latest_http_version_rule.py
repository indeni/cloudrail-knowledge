from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_http_version_rule import FunctionAppUseLatestHttpVersionRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppUseLatestHttpVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseLatestHttpVersionRule()

    def test_functionapp_no_site_config_block(self):
        self.run_test_case('function_app_no_site_config_block', True)

    def test_functionapp_http2_not_enabled(self):
        self.run_test_case('functionapp_http2_not_enabled', True)

    def test_functionapp_http2_enabled(self):
        self.run_test_case('functionapp_http2_enabled', False)
