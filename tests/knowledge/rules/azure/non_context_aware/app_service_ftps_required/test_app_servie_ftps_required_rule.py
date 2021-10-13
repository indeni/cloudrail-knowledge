from cloudrail.knowledge.rules.azure.non_context_aware.app_service_ftps_required_rule import AppServiceFtpsRequiredRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceFtpsRequiredRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceFtpsRequiredRule()

    def test_ftps_only(self):
        self.run_test_case('ftps_only', should_alert=False)

    def test_no_site_config(self):
        self.run_test_case('no_site_config', should_alert=True)

    def test_all_allowed(self):
        self.run_test_case('all_allowed', should_alert=True)

    def test_disabled(self):
        self.run_test_case('disabled', should_alert=False)
