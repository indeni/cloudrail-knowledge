from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_rds_instance_encrypt_at_rest_rule \
    import RdsEncryptAtRestRule


class TestRdsEncryptAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return RdsEncryptAtRestRule()

    def test_rds_encrypt_at_rest_disabled(self):
        rule_result = self.run_test_case('encrypt_at_rest_disabled', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Instance `aws_db_instance.default` is not set to use encrypt at rest" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS Instance')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_db_instance.default')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'RDS Instance')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_db_instance.default')

    def test_rds_encrypt_at_rest_enabled(self):
        self.run_test_case('encrypt_at_rest_enabled', False)

    def test_rds_cluster_encrypt_at_rest_disabled(self):
        rule_result = self.run_test_case('cluster_encrypt_at_rest_disabled', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS DB cluster `aws_rds_cluster.default` is not set to use encrypt at rest" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS DB cluster')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_rds_cluster.default')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'RDS DB cluster')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_rds_cluster.default')

    def test_rds_cluster_encrypt_at_rest_enabled(self):
        self.run_test_case('cluster_encrypt_at_rest_enabled', False)

    def test_rds_global_cluster_encrypt_at_rest_disabled(self):
        rule_result = self.run_test_case('global_cluster_encrypt_at_rest_disabled', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Global Cluster `aws_rds_global_cluster.global` is not set to use encrypt at rest" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS Global Cluster')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_rds_global_cluster.global')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'RDS Global Cluster')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_rds_global_cluster.global')

    def test_rds_global_cluster_encrypt_at_rest_disabled_with_source_db_encrypted(self):
        self.run_test_case('global_cluster_encrypt_at_rest_disabled_with_source_db_encrypted', False)

    def test_rds_global_cluster_encrypt_at_rest_disabled_with_source_db_not_encrypted(self):
        rule_result = self.run_test_case('global_cluster_encrypt_at_rest_disabled_with_source_db_not_encrypted', True, 2)
        self.assertIsNotNone(rule_result)
        rds_cluster = next((cluster for cluster in rule_result.issues if cluster.exposed.get_type() == 'RDS DB cluster'), None)
        rds_global_cluster = next((cluster for cluster in rule_result.issues if cluster.exposed.get_type() == 'RDS Global Cluster'), None)
        self.assertIsNotNone(rds_cluster)
        self.assertIsNotNone(rds_global_cluster)
        self.assertTrue(("RDS DB cluster" in rds_cluster.evidence and
                         "is not set to use encrypt at rest" in rds_cluster.evidence))
        self.assertEqual(rds_cluster.exposed.get_type(), 'RDS DB cluster')
        self.assertEqual(rds_cluster.violating.get_type(), 'RDS DB cluster')
        self.assertTrue(("RDS Global Cluster" in rds_global_cluster.evidence and
                         "is not set to use encrypt at rest" in rds_global_cluster.evidence))
        self.assertEqual(rds_global_cluster.exposed.get_type(), 'RDS Global Cluster')
        self.assertEqual(rds_global_cluster.violating.get_type(), 'RDS Global Cluster')

    def test_rds_global_cluster_encrypt_at_rest_enabled(self):
        self.run_test_case('global_cluster_encrypt_at_rest_enabled', False)
