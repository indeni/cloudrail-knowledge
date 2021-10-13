from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_neptune_cluster_encrypted_at_rest_rule_with_customer_managed_cmk import \
    EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule()

    def test_encrypted_aws_managed_cmk_by_default(self):
        self.run_test_case('encrypted_aws_managed_cmk_by_default', True)

    def test_encrypted_aws_managed_cmk_by_key_arn(self):
        self.run_test_case('encrypted_aws_managed_cmk_by_key_arn', True)

    def test_encrypted_customer_managed_cmk_creating_key(self):
        self.run_test_case('encrypted_customer_managed_cmk_creating_key', False)

    def test_encrypted_customer_managed_cmk_existing_key(self):
        self.run_test_case('encrypted_customer_managed_cmk_existing_key', False)
