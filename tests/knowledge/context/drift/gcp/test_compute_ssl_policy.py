from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseGcpDriftTest, drift_test


class TestComputeSslPolicyDrifts(BaseGcpDriftTest):

    def get_component(self):
        return 'compute/compute_ssl_policy'

    @drift_test(module_path="ssl_policy_profile")
    def test_change_ssl_policy_profile(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        change_ssl_policy = next(change_ssl_policy for change_ssl_policy in results if change_ssl_policy.resource_id == 'google_compute_ssl_policy.ssl_policy')
        self.assertEqual(change_ssl_policy.resource_iac['profile'], 'MODERN')
        self.assertEqual(change_ssl_policy.resource_live['profile'], 'COMPATIBLE')
