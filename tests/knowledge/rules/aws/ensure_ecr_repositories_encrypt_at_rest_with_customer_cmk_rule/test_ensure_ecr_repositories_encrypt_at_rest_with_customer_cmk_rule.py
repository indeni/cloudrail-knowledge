from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_ecr_repositories_encrypt_at_rest_with_customer_cmk_rule import\
    EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule()

    def test_default_encryption(self):
        self.run_test_case('default_encryption', True)

    def test_encrypted_using_aws_key(self):
        self.run_test_case('encrypted_using_aws_key', True)

    def test_encrypted_cmk_new_key(self):
        self.run_test_case('encrypted_cmk_new_key', False)
