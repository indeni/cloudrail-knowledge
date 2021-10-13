from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .ensure_rds_cluster_instances_encrypted_at_rest_rule_with_customer_managed_cmk import \
    EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest

class TestEnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule()

    def test_rds_cluster_instance_insights_encrypted_with_customer_managed_cmk_creating_key(self):
        self.run_test_case('rds_cluster_instance_insights_encrypted_with_customer_managed_cmk_creating_key', False)

    def test_rds_cluster_instance_insights_encrypted_with_customer_managed_cmk_existing_key(self):
        self.run_test_case('rds_cluster_instance_insights_encrypted_with_customer_managed_cmk_existing_key', False)

    def test_rds_cluster_instance_insights_encrypted_with_aws_managed_cmk_by_key_arn(self):
        rule_result = self.run_test_case('rds_cluster_instance_insights_encrypted_with_aws_managed_cmk_by_key_arn', True, 2)
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue('is not set to be encrypted at rest using customer-managed CMK' in item.evidence)
            self.assertTrue('RDS Instance' in (item.exposed.get_type(), item.violating.get_type()))
