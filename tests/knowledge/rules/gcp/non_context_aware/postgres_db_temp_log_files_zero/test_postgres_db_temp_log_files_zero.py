from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.postgres_database_temp_log_files_zero_rule import PostgresDatabaseTempLogFilesZeroRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPostgresDbTempLogFilesZero(GcpBaseRuleTest):

    def get_rule(self):
        return PostgresDatabaseTempLogFilesZeroRule()

    @rule_test('log_temp_files_on', should_alert=True)
    def test_log_temp_files_on(self, rule_result: RuleResponse):
        pass

    @rule_test('log_temp_files_off', should_alert=False)
    def test_log_min_duration_off(self, rule_result: RuleResponse):
        pass
