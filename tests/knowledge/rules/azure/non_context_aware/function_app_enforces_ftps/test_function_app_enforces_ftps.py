from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestFunctionAppEnforcesFtps(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppEnforcesFtpsOnlyRule()

    def test_ftps_enabled(self):
        self.run_test_case('ftps_enabled',
                           should_alert=False)

    def test_ftps_disabled(self):
        self.run_test_case('ftps_disabled',
                           should_alert=True)
