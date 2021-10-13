from cloudrail.knowledge.rules.aws.non_context_aware.backup_checks.ensure_rds_resource_backup_retention_enabled_rule import \
    EnsureRdsResourceBackupRetentionEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRdsResourceBackupRetentionEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsResourceBackupRetentionEnabledRule()

    def test_rds_cluster_retention_disabled(self):
        self.run_test_case('rds_cluster_retention_disabled', True)

    def test_rds_cluster_retention_set(self):
        self.run_test_case('rds_cluster_retention_set', False)

    def test_rds_instance_no_retention(self):
        self.run_test_case('rds_instance_no_retention', True)

    def test_rds_instance_retention_set(self):
        self.run_test_case('rds_instance_retention_set', False)
