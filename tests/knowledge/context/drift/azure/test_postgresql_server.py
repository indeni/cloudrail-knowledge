from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestPostgresqlServer(BaseAzureDriftTest):

    def get_component(self):
        return 'postgresql_server'

    @drift_test(module_path="ssl_enforcement_enabled")
    def test_function_app_modify_tls_version(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        postgresql_server = next(res for res in results if res.resource_id == 'azurerm_postgresql_server.example')
        self.assertEqual(True, postgresql_server.resource_iac['ssl_enforcement_enabled'])
        self.assertEqual(False, postgresql_server.resource_live['ssl_enforcement_enabled'])
