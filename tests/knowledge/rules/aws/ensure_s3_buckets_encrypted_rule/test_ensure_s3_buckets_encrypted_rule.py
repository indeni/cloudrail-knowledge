from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_encrypted_rule import \
    EnsureS3BucketsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureS3BucketsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketsEncryptedRule()

    # def test_encrypted(self):
    #     self.run_test_case('encrypted', False)

    def test_non_encrypted(self):
        self.run_test_case('non_encrypted', True)

    def test_non_encrypted_public_bucket(self):
        self.run_test_case('non_encrypted_public_bucket', False)

    def test_un_encrypt_public_bucket_with_cloudfront_private_connection(self):
        self.run_test_case('un-encrypt-public-bucket-with-cloudfront-private-connection', True)
