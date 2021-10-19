from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_all_resources_tagged_rule import EnsureAllResourcesTaggedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureAllResourcesTaggedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAllResourcesTaggedRule()

    @rule_test('2_items_without_tags', True, 2)
    def test_2_items_without_tags(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        sqs_evidence = next((sns for sns in rule_result.issues if sns.exposed.get_type() == 'SQS queue'), None)
        sns_evidence = next((sns for sns in rule_result.issues if sns.exposed.get_type() == 'SNS topic'), None)
        self.assertIsNotNone(sqs_evidence)
        self.assertIsNotNone(sns_evidence)
        self.assertTrue(all("does not have any tags set" in item.evidence for item in rule_result.issues))

    @rule_test('2_items_with_only_name_tag', True, 2)
    def test_2_items_with_only_name_tag(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        sqs_evidence = next((sns for sns in rule_result.issues if sns.exposed.get_type() == 'SQS queue'), None)
        sns_evidence = next((sns for sns in rule_result.issues if sns.exposed.get_type() == 'SNS topic'), None)
        self.assertIsNotNone(sqs_evidence)
        self.assertIsNotNone(sns_evidence)
        self.assertTrue(all('does not have any tags set other than "Name"' in item.evidence for item in rule_result.issues))

    @rule_test('2_items_with_tags', False)
    def test_2_items_with_tags(self, rule_result: RuleResponse):
        pass

    @rule_test('Athena_with_tags_s3_bucket_without_tags', True)
    def test_1_item_with_tags_1_without_tags(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("does not have any tags set" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'cloudrail-wg-encrypted-sse-s3-tags-test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'S3 Bucket')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'cloudrail-wg-encrypted-sse-s3-tags-test')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'S3 Bucket')
