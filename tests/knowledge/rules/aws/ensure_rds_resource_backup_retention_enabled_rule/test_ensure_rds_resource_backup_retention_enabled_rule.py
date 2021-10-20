from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.backup_checks.ensure_rds_resource_backup_retention_enabled_rule import \
    EnsureRdsResourceBackupRetentionEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureRdsResourceBackupRetentionEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsResourceBackupRetentionEnabledRule()

    @rule_test('rds_cluster_retention_disabled', True)
    def test_rds_cluster_retention_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('rds_cluster_retention_set', False)
    def test_rds_cluster_retention_set(self, rule_result: RuleResponse):
        pass

    @rule_test('rds_instance_no_retention', True)
    def test_rds_instance_no_retention(self, rule_result: RuleResponse):
        pass

    @rule_test('rds_instance_retention_set', False)
    def test_rds_instance_retention_set(self, rule_result: RuleResponse):
        pass
