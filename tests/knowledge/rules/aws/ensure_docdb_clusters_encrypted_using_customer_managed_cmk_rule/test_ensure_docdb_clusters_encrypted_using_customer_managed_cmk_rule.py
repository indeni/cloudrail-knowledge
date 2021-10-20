from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_docdb_clusters_encrypted_customer_managed_cmk_rule import \
    EnsureDocdbClustersEncryptedCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureDocdbClustersEncryptedCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedCustomerManagedCmkRule()

    @rule_test('docdb_cluster_encrypted_at_rest_using_cmk_not_customer_managed', True)
    def test_docdb_cluster_encrypted_at_rest_using_cmk_not_customer_managed(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_cluster_encrypted_at_rest_using_customer_managed_cmk_already_defined', False)
    def test_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk_already_defined(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_cluster_encrypted_at_rest_using_not_customer_managed_cmk_already_defined', True)
    def test_docdb_cluster_encrypted_at_rest_using_not_customer_managed_cmk_already_defined(self, rule_result: RuleResponse):
        pass

    @rule_test('docdb_cluster_encrypted_without_kms_key', True)
    def test_docdb_cluster_encrypted_without_kms_key(self, rule_result: RuleResponse):
        pass
