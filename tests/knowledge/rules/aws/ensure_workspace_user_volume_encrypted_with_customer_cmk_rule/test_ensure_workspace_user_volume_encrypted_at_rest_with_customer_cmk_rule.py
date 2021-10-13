from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .ensure_workspace_user_volume_encrypted_with_customer_cmk_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest



class TestEnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule()

    def test_user_volume_encrypted_with_aws_managed_cmk(self):
        self.run_test_case('user_volume_encrypted_with_aws_managed_cmk', True)

    def test_user_volume_encrypted_with_customer_managed_cmk_creating_key(self):
        self.run_test_case('user_volume_encrypted_with_customer_managed_cmk_creating_key', False)

    def test_user_volume_encrypted_with_customer_managed_cmk_existing_key(self):
        self.run_test_case('user_volume_encrypted_with_customer_managed_cmk_existing_key', False)
