from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestEc2Drifts(BaseAwsDriftTest):

    def get_component(self):
        return 'ec2'

    @drift_test(module_path="ec2_instance/changing_default_sg")
    def test_changing_default_sg(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        ec2 = next(ec2 for ec2 in results if ec2.resource_id == 'aws_instance.web')
        self.assertEqual(ec2.resource_iac['security_group_ids'], ['default'])
        self.assertEqual(ec2.resource_live['security_group_ids'], ['sg-00aa995205a07db73'])
