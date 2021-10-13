from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from test.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestStorageAccount(BaseAzureDriftTest):

    def get_component(self):
        return 'my_sql_server'

    @drift_test(module_path="ssl_enforcement_enabled")
    def test_ssl_enforcement_enabled(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        storage_account = next(res for res in results if res.resource_id == 'azurerm_mysql_server.example')
        self.assertEqual(True, storage_account.resource_iac['ssl_enforcement_enabled'])
        self.assertEqual(False, storage_account.resource_live['ssl_enforcement_enabled'])
