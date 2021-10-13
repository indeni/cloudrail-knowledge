from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_ssm_parameter_store_using_encrypted_customer_managed_kms_rule import \
    EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule()

    def test_default_encryption(self):
        self.run_test_case('default_encryption', True)

    def test_encrypted_aws_managed_key_arn(self):
        self.run_test_case('encrypted_aws_managed_key_arn', True)

    def test_encrypted_customer_kms_creating(self):
        self.run_test_case('encrypted_customer_kms_creating', False)

    def test_encrypted_customer_kms_existing_key(self):
        self.run_test_case('encrypted_customer_kms_existing_key', False)
