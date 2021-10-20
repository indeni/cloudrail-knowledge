from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestAutoProvision(BaseAzureDriftTest):

    def get_component(self):
        return 'auto_provision'

    @drift_test(module_path="log_analytics_agent")
    def test_log_analytics_agent(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        auto_provision = next(res for res in results if res.resource_id == 'azurerm_security_center_auto_provisioning.example')
        self.assertTrue(auto_provision.resource_iac['auto_provision_is_on'])
        self.assertFalse(auto_provision.resource_live['auto_provision_is_on'])
