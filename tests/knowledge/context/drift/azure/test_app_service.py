from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestAppService(BaseAzureDriftTest):

    def get_component(self):
        return 'app_service'

    @drift_test(module_path="https_only_modification")
    def test_app_service_https_only(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        app_service = next(res for res in results if res.resource_id == 'azurerm_app_service.webapp')
        self.assertEqual(True, app_service.resource_iac['https_only'])
        self.assertEqual(False, app_service.resource_live['https_only'])
