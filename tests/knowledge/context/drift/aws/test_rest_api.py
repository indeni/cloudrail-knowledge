from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from test.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestRestApi(BaseAwsDriftTest):

    def get_component(self):
        return 'rest_api'

    @drift_test(module_path="delete_method")
    def test_delete_method(self, results: List[Drift]):
        self.assertTrue(len(results), 1)
        rest_api = next(res for res in results if res.resource_id == 'aws_api_gateway_rest_api.api_gw')
        self.assertIsNotNone(rest_api)
        self.assertTrue(len(rest_api.resource_iac['api_gateway_methods']) > len(rest_api.resource_live['api_gateway_methods']))

    @drift_test(module_path="modify_endpoint_type")
    def test_modify_endpoint_type(self, results: List[Drift]):
        self.assertTrue(len(results), 1)
        rest_api = next(res for res in results if res.resource_id == 'aws_api_gateway_rest_api.api_gw')
        self.assertIsNotNone(rest_api)
        self.assertTrue(rest_api.resource_iac['api_gateway_type'].get('value') == 'REGIONAL')
        self.assertTrue(rest_api.resource_live['api_gateway_type'].get('value') == 'PRIVATE')
