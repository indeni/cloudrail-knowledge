from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_client_certificates_required_in_web_app_rule import \
    AppServiceClientCertificatesRequiredRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceFtpsRequiredRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceClientCertificatesRequiredRule()

    def test_ftps_only(self):
        self.run_test_case('webapp_client_cert_enabled', should_alert=False)

    def test_no_site_config(self):
        self.run_test_case('webapp_client_cert_not_enabled', should_alert=True)

