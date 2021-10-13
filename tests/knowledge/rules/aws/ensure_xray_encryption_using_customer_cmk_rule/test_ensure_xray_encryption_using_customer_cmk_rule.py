from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_xray_encryption_using_customer_cmk_rule import \
    EnsureXrayEncryptionCmkRule


class TestEnsureXrayEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureXrayEncryptionCmkRule()

    def test_kms_key_arn_aws_managed(self):
        self.run_test_case('kms_key_arn_aws_managed', True)

    def test_no_kms_encryption(self):
        self.run_test_case('no_kms_encryption', True)

    def test_kms_key_customer_creating(self):
        self.run_test_case('kms_key_customer_creating', False)

    def test_kms_key_customer_existing(self):
        self.run_test_case('kms_key_customer_existing', False)
