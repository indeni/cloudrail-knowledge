from cloudrail.knowledge.rules.azure.context_aware.key_vault_diagnostic_logs_enabled_rule import KeyVaultDiagnosticLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestKeyVaultDiagnosticLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KeyVaultDiagnosticLogsEnabledRule()

    def test_log_and_retention_enabled_default_days(self):
        self.run_test_case('log_and_retention_enabled_default_days', False)

    def test_logs_and_retention_enabled(self):
        self.run_test_case('logs_and_retention_enabled', False)

    def test_log_enabled_retention_disabled(self):
        rule_result = self.run_test_case('log_enabled_retention_disabled', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('have a disabled log retention policy' in rule_result.issues[0].evidence)

    def test_logs_not_defined(self):
        rule_result = self.run_test_case('logs_not_defined', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have log block configuration' in rule_result.issues[0].evidence)

    def test_key_vault_no_monitoring(self):
        rule_result = self.run_test_case('key_vault_no_monitoring', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have diagnostic settings' in rule_result.issues[0].evidence)

    def test_logs_configured_not_enabled(self):
        rule_result = self.run_test_case('logs_configured_not_enabled', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have log enabled' in rule_result.issues[0].evidence)

    def test_no_retention_policy(self):
        rule_result = self.run_test_case('no_retention_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have a log retention policy' in rule_result.issues[0].evidence)

    def test_log_configureed_retention_days_violating(self):
        rule_result = self.run_test_case('log_configureed_retention_days_violating', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('does not have a log retention policy days equal to 0 or greater than or equal to 365' in rule_result.issues[0].evidence)
