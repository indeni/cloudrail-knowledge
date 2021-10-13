from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dynamodb_tables_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule()

    def test_encrypted_customer_managed_new_key(self):
        self.run_test_case('encrypted_customer_managed_new_key', False)

    def test_encrypted_default_aws_managed(self):
        self.run_test_case('encrypted_default_aws_managed', True)

    def test_encrypted_default_aws_by_key_arn(self):
        self.run_test_case('encrypted_default_aws_by_key_arn', True)

    def test_no_encryption_at_all(self):
        self.run_test_case('no_encryption_at_all', True)
