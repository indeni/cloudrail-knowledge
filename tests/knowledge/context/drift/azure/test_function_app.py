from typing import List

from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState
from cloudrail.knowledge.drift_detection.drift_detection_result import Drift

from tests.knowledge.context.drift.base_drift_test import BaseAzureDriftTest, drift_test


class TestFunctionApp(BaseAzureDriftTest):

    def get_component(self):
        return 'function_app'

    @drift_test(module_path="https_only")
    def test_function_app_https_only(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        functionapp = next(res for res in results if res.resource_id == 'azurerm_function_app.functionapp')
        self.assertEqual(True, functionapp.resource_iac['https_only'])
        self.assertEqual(False, functionapp.resource_live['https_only'])

    @drift_test(module_path="modify_tls")
    def test_function_app_modify_tls_version(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        functionapp = next(res for res in results if res.resource_id == 'azurerm_function_app.functionapp')
        self.assertEqual('1.2', functionapp.resource_iac['app_service_config']['minimum_tls_version'])
        self.assertEqual('1.1', functionapp.resource_live['app_service_config']['minimum_tls_version'])

    @drift_test(module_path="ftps_only_usage")
    def test_ftps_only_usage(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        functionapp = next(res for res in results if res.resource_id == 'azurerm_function_app.functionapp')
        self.assertEqual(functionapp.resource_iac['app_service_config']['ftps_state'], FtpsState.FTPS_ONLY.value)
        self.assertEqual(functionapp.resource_live['app_service_config']['ftps_state'], FtpsState.ALL_ALLOWED.value)

    @drift_test(module_path="authentication_enabled")
    def test_authentication_enabled(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        functionapp = next(res for res in results if res.resource_id == 'azurerm_function_app.functionapp')
        self.assertTrue(functionapp.resource_iac['app_service_config']['auth_settings']['enabled'])
        self.assertFalse(functionapp.resource_live['app_service_config']['auth_settings']['enabled'])
