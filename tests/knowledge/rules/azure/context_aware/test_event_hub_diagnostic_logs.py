import unittest

from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import EventHubNamespaceDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEventHubDiagnosticLogsEnabled(unittest.TestCase):

    def setUp(self):
        self.rule = EventHubNamespaceDiagnosticLogsEnabledRule()

    @parameterized.expand(
        [
            ['No monitoring settings',
             None, True],
            ['No logs',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id', None), True],
            ['Logs enabled, but no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id', AzureMonitorDiagnosticLogsSettings(True, None)), True],
            ['Logs disabled, no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id', AzureMonitorDiagnosticLogsSettings(False, None)), True],
            ['Logs disabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None))),
             True],
            ['Logs disabled, retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0))),
             True],
            ['Logs enabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None))),
             True],
            ['Logs and retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0))),
             False],
            ['Logs and retention policy enabled, 0<days<365',
             AzureMonitorDiagnosticSetting('settings_name', 'event_hub_namespace_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 10))),
             True],
        ]
    )
    def test_states(self, unused_name: str, monitor_diagnostic_settings: AzureMonitorDiagnosticSetting, should_alert: bool):
        # Arrange
        event_hub_namespace: AzureEventHubNamespace = create_empty_entity(AzureEventHubNamespace)
        event_hub_namespace.name = 'event_hub_namespace-name'
        event_hub_namespace.set_id('event_hub_namespace_id')
        event_hub_namespace.with_aliases(event_hub_namespace.get_id())
        event_hub_namespace.get_monitor_settings().extend([monitor_diagnostic_settings] if monitor_diagnostic_settings else [])

        context = AzureEnvironmentContext(event_hub_namespaces=AliasesDict(event_hub_namespace),
                                          monitor_diagnostic_settings=AliasesDict(*event_hub_namespace.get_monitor_settings().copy()))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
