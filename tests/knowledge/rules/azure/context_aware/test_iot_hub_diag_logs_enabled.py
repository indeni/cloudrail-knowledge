import unittest

from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import AzureIoTHub
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import IotHubDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from parameterized import parameterized


class TestIotHubDiagnosticLogsEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = IotHubDiagnosticLogsEnabledRule()

    monitor_diagnostic_settings: AzureMonitorDiagnosticSetting = create_empty_entity(AzureMonitorDiagnosticSetting)
    @parameterized.expand(
        [
            ['No monitoring settings', monitor_diagnostic_settings, True],
            ['No logs',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key', None), True],
            ['Logs enabled, but no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key', AzureMonitorDiagnosticLogsSettings(True, None)), True],
            ['Logs disabled, no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key', AzureMonitorDiagnosticLogsSettings(False, None)), True],
            ['Logs disabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None))), True],
            ['Logs disabled, retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0))), True],
            ['Logs enabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None))), True],
            ['Logs and retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0))), False],
            ['Logs and retention policy enabled, 0<days<365',
             AzureMonitorDiagnosticSetting('settings_name', 'diag_monitor_setting_key', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 10))), True],
        ]
    )
    def test_states(self, unused_name: str, monitor_diagnostic_settings: AzureMonitorDiagnosticSetting, should_alert: bool):
        # Arrange
        iot_hub: AzureIoTHub = create_empty_entity(AzureIoTHub)
        iot_hub.name = 'tmp-name'
        iot_hub.set_id('diag_monitor_setting_key')
        iot_hub.with_aliases(iot_hub.get_id())
        iot_hub.monitor_diagnostic_settings = [monitor_diagnostic_settings] if monitor_diagnostic_settings else []

        context = AzureEnvironmentContext(iot_hubs=AliasesDict(iot_hub),
                                          monitor_diagnostic_settings=AliasesDict(monitor_diagnostic_settings))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)