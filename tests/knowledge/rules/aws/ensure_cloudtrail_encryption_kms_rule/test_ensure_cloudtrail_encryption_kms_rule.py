from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloudtrail_encryption_kms_rule import \
    EnsureCloudTrailEncryptionKmsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudTrailEncryptionKmsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudTrailEncryptionKmsRule()

    def test_encrypted(self):
        self.run_test_case('encrypted', False)

    def test_non_encrypted(self):
        self.run_test_case('non_encrypted', True)
