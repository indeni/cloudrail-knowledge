from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_elasticache_redis_cluster_auto_backup_enabled_rule import \
    EnsureElasticacheRedisClusterAutoBackupEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureElasticacheRedisClusterAutoBackupEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticacheRedisClusterAutoBackupEnabledRule()

    @rule_test('auto-backup-disabled-with-param', True)
    def test_auto_backup_disabled_with_param(self, rule_result: RuleResponse):
        pass

    @rule_test('auto_backup_enabled', False)
    def test_auto_backup_enabled(self, rule_result: RuleResponse):
        pass
