from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.vmss_diagnostics_logs_enabled_rule import VmssDiagnosticsLogsEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestVmssDiagnosticsLogsEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return VmssDiagnosticsLogsEnabledRule()

    @rule_test('vmss_linux_az_diagnostic_log_enabled', should_alert=False)
    def test_vmss_linux_az_diagnostic_log_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('vmss_linux_diagnostic_log_disabled', should_alert=True)
    def test_vmss_linux_diagnostic_log_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('vmss_linux_ostc_diagnostic_log_enabled', should_alert=False)
    def test_vmss_linux_ostc_diagnostic_log_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('vmss_win_diagnostic_log_disabled', should_alert=True)
    def test_vmss_win_diagnostic_log_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('vmss_win_diagnostic_log_enabled', should_alert=False)
    def test_vmss_win_diagnostic_log_enabled(self, rule_result: RuleResponse):
        pass
