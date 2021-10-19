from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_neptune_cluster_encrypted_at_rest_rule_with_customer_managed_cmk import \
    EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule()

    @rule_test('encrypted_aws_managed_cmk_by_default', True)
    def test_encrypted_aws_managed_cmk_by_default(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_aws_managed_cmk_by_key_arn', True)
    def test_encrypted_aws_managed_cmk_by_key_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_customer_managed_cmk_creating_key', False)
    def test_encrypted_customer_managed_cmk_creating_key(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_customer_managed_cmk_existing_key', False)
    def test_encrypted_customer_managed_cmk_existing_key(self, rule_result: RuleResponse):
        pass
