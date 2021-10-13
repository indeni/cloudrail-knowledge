from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestRds(BaseAwsDriftTest):

    def get_component(self):
        return 'rds'

    @drift_test(module_path="disable_performance_insights")
    def test_disable_performance_insights(self, results: List[Drift]):
        rds = next(res for res in results if res.resource_id == 'aws_db_instance.test')
        self.assertTrue(rds.resource_iac['performance_insights_enabled'])
        self.assertFalse(rds.resource_live['performance_insights_enabled'])
