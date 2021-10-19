from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_object_encrypted_rule import \
    EnsureS3BucketObjectsEncryptedRule


class TestEnsureS3BucketObjectsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketObjectsEncryptedRule()

    @rule_test('encrypted_aes256', False)
    def test_encrypted_aes256(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_aws_kms', False)
    def test_encrypted_aws_kms(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted', True)
    def test_non_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('multiple_encrypted_objects', True, 10)
    def test_multiple_encrypted_objects(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_on_public_bucket', False)
    def test_non_encrypted_on_public_bucket(self, rule_result: RuleResponse):
        pass
