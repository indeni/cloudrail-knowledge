from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .ensure_workspace_user_volume_encrypted_with_customer_cmk_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule()

    @rule_test('user_volume_encrypted_with_aws_managed_cmk', True)
    def test_user_volume_encrypted_with_aws_managed_cmk(self, rule_result: RuleResponse):
        pass

    @rule_test('user_volume_encrypted_with_customer_managed_cmk_creating_key', False)
    def test_user_volume_encrypted_with_customer_managed_cmk_creating_key(self, rule_result: RuleResponse):
        pass

    @rule_test('user_volume_encrypted_with_customer_managed_cmk_existing_key', False)
    def test_user_volume_encrypted_with_customer_managed_cmk_existing_key(self, rule_result: RuleResponse):
        pass
