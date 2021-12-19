from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseGcpDriftTest, drift_test


class TestComputeSubNetworkDrifts(BaseGcpDriftTest):

    def get_component(self):
        return 'compute_subnetwork'

    @drift_test(module_path="change_cidr")
    def test_change_cidr(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        change_subnetwork = next(change_subnetwork for change_subnetwork in results if change_subnetwork.resource_id == 'google_compute_subnetwork.subnet-logging3')
        self.assertEqual(change_subnetwork.resource_iac['ip_cidr_range'], '10.3.0.0/24')
        self.assertEqual(change_subnetwork.resource_live['ip_cidr_range'], '10.3.0.0/16')

    @drift_test(module_path="change_flow_logs")
    def test_change_flow_logs(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        change_subnetwork = next(change_subnetwork for change_subnetwork in results if change_subnetwork.resource_id == 'google_compute_subnetwork.subnet-logging3')
        self.assertFalse(change_subnetwork.resource_iac['log_config']['enabled'])
        self.assertTrue(change_subnetwork.resource_live['log_config']['enabled'])
