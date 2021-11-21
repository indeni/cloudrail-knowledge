from typing import List
from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseGcpDriftTest


class TestComputeInstance(BaseGcpDriftTest):

    def get_component(self):
        return 'compute'

    @drift_test(module_path="compute_instance/enable_public_ip")
    def test_changing_default_sg(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        drift: Drift = results[0]
        self.assertEqual(drift.resource_id, 'google_compute_instance.drift_resource')
        self.assertEqual(len(drift.resource_live.get('network_interfaces', [])), 1)
        self.assertEqual(len(drift.resource_live.get('network_interfaces')[0].get('access_config')), 1)

        self.assertEqual(len(drift.resource_iac.get('network_interfaces', [])), 1)
        self.assertEqual(len(drift.resource_iac.get('network_interfaces')[0].get('access_config')), 0)
