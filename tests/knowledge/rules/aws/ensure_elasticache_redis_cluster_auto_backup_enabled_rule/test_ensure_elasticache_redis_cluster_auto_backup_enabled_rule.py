from cloudrail.knowledge.rules.aws.non_context_aware.ensure_elasticache_redis_cluster_auto_backup_enabled_rule import \
    EnsureElasticacheRedisClusterAutoBackupEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureElasticacheRedisClusterAutoBackupEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheRedisClusterAutoBackupEnabledRule()

    def test_auto_backup_disabled_with_param(self):
        self.run_test_case('auto-backup-disabled-with-param', True)

    def test_auto_backup_enabled(self):
        self.run_test_case('auto_backup_enabled', False)
