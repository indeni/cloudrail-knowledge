from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .ensure_secrets_manager_secrets_encrypted_at_rest_with_customer_amanaged_cmk_rule import \
    EnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule()

    def test_secretsmanager_secrets_encrypted_at_rest_with_aws_managed_key_by_default(self):
        self.run_test_case('secretsmanager_secrets_encrypted_at_rest_with_aws_managed_key_by_default', True)

    def test_secretsmanager_secrets_encrypted_at_rest_with_aws_managed_key_by_key_arn(self):
        self.run_test_case('secretsmanager_secrets_encrypted_at_rest_with_aws_managed_key_by_key_arn', True)

    def test_secretsmanager_secrets_encrypted_at_rest_with_customer_managed_key_creating_key(self):
        self.run_test_case('secretsmanager_secrets_encrypted_at_rest_with_customer_managed_key_creating_key', False)

    def test_secretsmanager_secrets_encrypted_at_rest_with_customer_managed_key_existing_key(self):
        self.run_test_case('secretsmanager_secrets_encrypted_at_rest_with_customer_managed_key_existing_key', False)
