from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestStorageAccount(BaseAzureDriftTest):

    def get_component(self):
        return 'storage_account'

    @drift_test(module_path="network_bypass_rule")
    def test_network_bypass_rule(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        storage_account = next(res for res in results if res.resource_id == 'azurerm_storage_account.storacc')
        self.assertEqual(['AzureServices'], storage_account.resource_iac['network_rules']['bypass_traffic'])
        self.assertEqual(['None'], storage_account.resource_live['network_rules']['bypass_traffic'])

    @drift_test(module_path="network_rules")
    def test_default_network_access_denied(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        storage_account = next(res for res in results if res.resource_id == 'azurerm_storage_account.storacc')
        self.assertEqual('ALLOW', storage_account.resource_live['network_rules']['default_action']['name'])
        self.assertEqual('DENY', storage_account.resource_iac['network_rules']['default_action']['name'])

    @drift_test(module_path="enable_https_traffic_only")
    def test_enable_https_traffic_only(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        storage_account = next(res for res in results if res.resource_id == 'azurerm_storage_account.storacc')
        self.assertEqual(False, storage_account.resource_live['enable_https_traffic_only'])
        self.assertEqual(True, storage_account.resource_iac['enable_https_traffic_only'])

    @drift_test(module_path="allow_blob_public_access")
    def test_enable_https_traffic_only(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        storage_account = next(res for res in results if res.resource_id == 'azurerm_storage_account.storacc')
        self.assertEqual(True, storage_account.resource_live['allow_blob_public_access'])
        self.assertEqual(False, storage_account.resource_iac['allow_blob_public_access'])
