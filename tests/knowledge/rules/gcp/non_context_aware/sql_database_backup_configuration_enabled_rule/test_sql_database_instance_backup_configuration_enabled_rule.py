from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_backup_configuration_enabled_rule import SqlDatabaseBackupConfigurationEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestSqlDatabaseBackupConfigurationEnabledRule(GcpBaseRuleTest):
    def get_rule(self):
        return SqlDatabaseBackupConfigurationEnabledRule()

    @rule_test('both_enabled', should_alert=False)
    def test_both_enabled_true(self, rule_result: RuleResponse):
        pass

    @rule_test('no_enabled', should_alert=True, number_of_issue_items=2)
    def test_no_enabled_true(self, rule_result: RuleResponse):
        pass

    @rule_test('one_enabled', should_alert=True)
    def test_one_enabled_true_one_enabled_false(self, rule_result: RuleResponse):
        pass
