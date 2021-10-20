from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestSqsQueuePolicy(BaseAwsDriftTest):

    def get_component(self):
        return 'sqs_policy'

    @drift_test(module_path="policy_statement_change")
    def test_policy_statement_change(self, results: List[Drift]):
        sqs_queue = next(res for res in results if res.resource_id == 'aws_sqs_queue.not-secure-q')
        self.assertEqual(sqs_queue.resource_live['resource_based_policy']['policy_statements'][0]['actions'], ['sqs:SendMessage'])
        self.assertEqual(sqs_queue.resource_iac['resource_based_policy']['policy_statements'][0]['actions'], ['sqs:*'])

    @drift_test(module_path="no_encryption_at_rest")
    def test_no_encryption_at_rest(self, results: List[Drift]):
        sqs_policy = next(res for res in results if res.resource_id == 'aws_sqs_queue.test')
        self.assertEqual(1, len(results))
        self.assertTrue(sqs_policy.resource_live['encrypted_at_rest'])
        self.assertFalse(sqs_policy.resource_iac['encrypted_at_rest'])

    @drift_test(module_path="sqs_no_policy")
    def test_sqs_no_policy(self, results: List[Drift]):
        sqs_policy = next(res for res in results if res.resource_id == 'aws_sqs_queue.test')
        self.assertTrue(sqs_policy.resource_live.get('resource_based_policy'))
        self.assertFalse(sqs_policy.resource_iac.get('resource_based_policy'))

    @drift_test(module_path="sqs_tags_change")
    def test_sqs_tags_change(self, results: List[Drift]):
        sqs_policy = next(res for res in results if res.resource_id == 'aws_sqs_queue.cloudrail')
        self.assertEqual(1, len(results))
        self.assertEqual(sqs_policy.resource_iac['tags']['Name'], 'Sqs Cloudrail Test')
        self.assertEqual(sqs_policy.resource_live['tags']['Name'], 'Testing drift')
