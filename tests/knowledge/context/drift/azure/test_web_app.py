from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestWebApp(BaseAzureDriftTest):

    def get_component(self):
        return 'web_app'

    @drift_test(module_path="ftps_state")
    def test_ftps_state(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        web_app = next((res for res in results if res.resource_id == 'azurerm_app_service.webapp'), None)
        self.assertEqual(web_app.resource_iac['app_service_config']['ftps_state'], 'FtpsOnly')
        self.assertEqual(web_app.resource_live['app_service_config']['ftps_state'], 'AllAllowed')

    @drift_test(module_path="authentication_check")
    def test_authentication_check(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        web_app = next((res for res in results if res.resource_id == 'azurerm_app_service.webapp'), None)
        self.assertTrue(web_app.resource_iac['app_service_config']['auth_settings']['enabled'])
        self.assertFalse(web_app.resource_live['app_service_config']['auth_settings']['enabled'])

    @drift_test(module_path="latest_tls")
    def test_latest_tls(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        web_app = next((res for res in results if res.resource_id == 'azurerm_app_service.webapp'), None)
        self.assertEqual(web_app.resource_iac['app_service_config']['minimum_tls_version'], '1.2')
        self.assertEqual(web_app.resource_live['app_service_config']['minimum_tls_version'], '1.1')
