from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_object_encrypted_rule import \
    EnsureS3BucketObjectsEncryptedRule


class TestEnsureS3BucketObjectsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketObjectsEncryptedRule()

    def test_encrypted_aes256(self):
        self.run_test_case('encrypted_aes256', False)

    def test_encrypted_aws_kms(self):
        self.run_test_case('encrypted_aws_kms', False)

    def test_non_encrypted(self):
        self.run_test_case('non_encrypted', True)

    def test_multiple_encrypted_objects(self):
        self.run_test_case('multiple_encrypted_objects', True, 10)

    def test_non_encrypted_on_public_bucket(self):
        self.run_test_case('non_encrypted_on_public_bucket', False)
