import unittest

from cloudrail.knowledge.context.azure.resources.keyvault.azure_key_vault import AzureKeyVault
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import KeyVaultDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from parameterized import parameterized


class TestKeyVaultDiagnosticLogsEnabled(unittest.TestCase):
    def setUp(self):
        self.rule = KeyVaultDiagnosticLogsEnabledRule()

    monitor_diagnostic_settings: AzureMonitorDiagnosticSetting = create_empty_entity(AzureMonitorDiagnosticSetting)
    @parameterized.expand(
        [
            ['No monitoring settings', monitor_diagnostic_settings, True],
            ['No logs',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', None, None), True],
            ['Logs enabled, but no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, None), None), True],
            ['Logs disabled, no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, None), None), True],
            ['Logs disabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None)), None), True],
            ['Logs disabled, retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0)), None), True],
            ['Logs enabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None)), None), True],
            ['Logs and retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0)), None), False],
            ['Logs and retention policy enabled, 0<days<365',
             AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 10)), None), True],
        ]
    )
    def test_states(self, unused_name: str, monitor_diagnostic_settings: AzureMonitorDiagnosticSetting, should_alert: bool):
        # Arrange
        key_vault: AzureKeyVault = create_empty_entity(AzureKeyVault)
        key_vault.name = 'tmp-name'
        key_vault.set_id('keyvault_id')
        key_vault.with_aliases(key_vault.get_id())
        key_vault.monitor_diagnostic_settings = [monitor_diagnostic_settings] if monitor_diagnostic_settings else []

        context = AzureEnvironmentContext(key_vaults=AliasesDict(key_vault),
                                          monitor_diagnostic_settings=AliasesDict(monitor_diagnostic_settings))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
