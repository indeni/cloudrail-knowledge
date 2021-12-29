from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import KeyVaultDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestKeyVaultDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KeyVaultDiagnosticLogsEnabledRule()

    @rule_test('log_and_retention_enabled_default_days', False)
    def test_log_and_retention_enabled_default_days(self, rule_result: RuleResponse):
        pass

    @rule_test('logs_and_retention_enabled', False)
    def test_logs_and_retention_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('log_enabled_retention_disabled', True)
    def test_log_enabled_retention_disabled(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('have a disabled log retention policy' in rule_result.issues[0].evidence)

    @rule_test('logs_not_defined', True)
    def test_logs_not_defined(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have log block configuration' in rule_result.issues[0].evidence)

    @rule_test('key_vault_no_monitoring', True)
    def test_key_vault_no_monitoring(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have diagnostic settings' in rule_result.issues[0].evidence)

    @rule_test('logs_configured_not_enabled', True)
    def test_logs_configured_not_enabled(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have log enabled' in rule_result.issues[0].evidence)

    @rule_test('no_retention_policy', True)
    def test_no_retention_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have a log retention policy' in rule_result.issues[0].evidence)

    @rule_test('log_configureed_retention_days_violating', True)
    def test_log_configureed_retention_days_violating(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have a log retention policy days equal to 0 or greater than or equal to 365' in rule_result.issues[0].evidence)
