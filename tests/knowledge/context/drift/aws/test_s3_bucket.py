from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from test.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestS3Bucket(BaseAwsDriftTest):

    def get_component(self):
        return 's3_bucket'

    @drift_test(module_path="adding_new_tag")
    def test_adding_new_tag_to_s3_bucket(self, results: List[Drift]):
        self.assertTrue(len(results), 1)
        s3_bucket = next(res for res in results if res.resource_id == 'aws_s3_bucket.b')
        self.assertTrue('new_test_tag_hashcode' not in s3_bucket.resource_iac['tags'])
        self.assertTrue('new_test_tag_hashcode' in s3_bucket.resource_live['tags'])

    @drift_test(module_path="s3_bucket_with_policy")
    def test_s3_bucket_modify_policy(self, results: List[Drift]):
        self.assertTrue(len(results), 1)
        s3_bucket = next(res for res in results if res.resource_id == 'aws_s3_bucket_policy.cloudrail-drift-test')
        self.assertEqual(s3_bucket.resource_live['statements'][0]['statement_id'], 'First')
        self.assertEqual(s3_bucket.resource_iac['statements'][0]['statement_id'], 'AllowRead')
