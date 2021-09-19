from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseDriftTest, drift_test


class TestSqsQueuePolicy(BaseDriftTest):

    def get_component(self):
        return 'sqs_policy'

    @drift_test(module_path="policy_statement_change")
    def test_policy_statement_change(self, results: List[Drift]):
        sqs_policy = next(res for res in results if res.resource_id == 'aws_sqs_queue_policy.secure-policy')
        self.assertEqual(sqs_policy.resource_live['statements'][0]['actions'], ['sqs:SendMessage'])
        self.assertEqual(sqs_policy.resource_iac['statements'][0]['actions'], ['sqs:*'])

    @drift_test(module_path="no_encryption_at_rest")
    def test_no_encryption_at_rest(self, results: List[Drift]):
        sqs_policy = next(res for res in results if res.resource_id == 'aws_sqs_queue.test')
        self.assertEqual(1, len(results))
        self.assertTrue(sqs_policy.resource_live['encrypted_at_rest'])
        self.assertFalse(sqs_policy.resource_iac['encrypted_at_rest'])
