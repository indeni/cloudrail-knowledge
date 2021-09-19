from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from test.knowledge.context.drift.base_drift_test import BaseDriftTest, drift_test


class TestLambdaFunction(BaseDriftTest):

    def get_component(self):
        return 'lambda_function'

    @drift_test(module_path="tracing_drift")
    def test_tracing_drift(self, results: List[Drift]):
        lambda_func = next(res for res in results if res.resource_id == 'aws_lambda_function.my-lambda')
        self.assertTrue(lambda_func.resource_live['xray_tracing_enabled'])
        self.assertFalse(lambda_func.resource_iac['xray_tracing_enabled'])
