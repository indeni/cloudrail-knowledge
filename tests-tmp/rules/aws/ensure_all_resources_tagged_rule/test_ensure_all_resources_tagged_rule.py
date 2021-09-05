from cloudrail.knowledge.rules.aws.non_context_aware.ensure_all_resources_tagged_rule import EnsureAllResourcesTaggedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureAllResourcesTaggedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAllResourcesTaggedRule()

    def test_2_items_without_tags(self):
        rule_result = self.run_test_case('2_items_without_tags', True, 2)
        self.assertIsNotNone(rule_result)
        sqs_evidence = next((sns for sns in rule_result.issue_items if sns.exposed.type == 'SQS queue'), None)
        sns_evidence = next((sns for sns in rule_result.issue_items if sns.exposed.type == 'SNS topic'), None)
        self.assertIsNotNone(sqs_evidence)
        self.assertIsNotNone(sns_evidence)
        self.assertTrue(all("does not have any tags set" in item.evidence for item in rule_result.issue_items))

    def test_2_items_with_only_name_tag(self):
        rule_result = self.run_test_case('2_items_with_only_name_tag', True, 2)
        self.assertIsNotNone(rule_result)
        sqs_evidence = next((sns for sns in rule_result.issue_items if sns.exposed.type == 'SQS queue'), None)
        sns_evidence = next((sns for sns in rule_result.issue_items if sns.exposed.type == 'SNS topic'), None)
        self.assertIsNotNone(sqs_evidence)
        self.assertIsNotNone(sns_evidence)
        self.assertTrue(all('does not have any tags set other than "Name"' in item.evidence for item in rule_result.issue_items))

    def test_2_items_with_tags(self):
        self.run_test_case('2_items_with_tags', False)

    def test_1_item_with_tags_1_without_tags(self):
        rule_result = self.run_test_case('Athena_with_tags_s3_bucket_without_tags', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("does not have any tags set" in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.name, 'cloudrail-wg-encrypted-sse-s3-tags-test')
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'S3 Bucket')
        self.assertEqual(rule_result.issue_items[0].violating.name, 'cloudrail-wg-encrypted-sse-s3-tags-test')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'S3 Bucket')
