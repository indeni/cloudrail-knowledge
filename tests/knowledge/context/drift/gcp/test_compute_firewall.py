from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseGcpDriftTest, drift_test


class TestComputeFirewallDrifts(BaseGcpDriftTest):

    def get_component(self):
        return 'compute_firewall'

    @drift_test(module_path="change_firewall_rules")
    def test_change_firewall_rules(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        change_firewall = next(change_firewall for change_firewall in results if change_firewall.resource_id == 'google_compute_firewall.default')
        self.assertEqual(change_firewall.resource_iac['source_ranges'], ['192.168.12.34/32'])
        self.assertEqual(change_firewall.resource_iac['source_tags'], ['web'])
        self.assertEqual(change_firewall.resource_live['source_ranges'], ['119.23.45.65/32'])
        self.assertEqual(change_firewall.resource_live['source_tags'], ['change-tags'])
