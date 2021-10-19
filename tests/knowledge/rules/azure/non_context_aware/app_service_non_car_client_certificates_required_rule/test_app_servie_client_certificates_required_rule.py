from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_non_car_client_certificates_required_in_web_app_rule import \
    AppServiceClientCertificatesRequiredRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceFtpsRequiredRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceClientCertificatesRequiredRule()

    @rule_test('webapp_client_cert_enabled', should_alert=False)
    def test_ftps_only(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_client_cert_not_enabled', should_alert=True)
    def test_no_site_config(self, rule_result: RuleResponse):
        pass

