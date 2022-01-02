import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_store import AzureDataLakeStore
from cloudrail.knowledge.rules.azure.context_aware.disgnostics_logs_enabled_rule import DataLakeStoreDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from parameterized import parameterized


class TestDataLakeStoreDiagnosticLogsEnabled(unittest.TestCase):

    def setUp(self):
        self.rule = DataLakeStoreDiagnosticLogsEnabledRule()

    @parameterized.expand(
        [
            ['No monitoring settings',
             None, True],
            ['No logs',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id', None, None), True],
            ['Logs enabled, but no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id', AzureMonitorDiagnosticLogsSettings(True, None), None), True],
            ['Logs disabled, no retention policy',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id', AzureMonitorDiagnosticLogsSettings(False, None), None), True],
            ['Logs disabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None)), None),
             True],
            ['Logs disabled, retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id',
                                           AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0)), None),
             True],
            ['Logs enabled, retention policy disabled',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(False, None)), None),
             True],
            ['Logs and retention policy enabled, days=0',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 0)), None),
             False],
            ['Logs and retention policy enabled, 0<days<365',
             AzureMonitorDiagnosticSetting('settings_name', 'datalakestore_id',
                                           AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True, 10)), None),
             True],
        ]
    )
    def test_states(self, unused_name: str, monitor_diagnostic_settings: AzureMonitorDiagnosticSetting, should_alert: bool):
        # Arrange
        data_lake_store: AzureDataLakeStore = create_empty_entity(AzureDataLakeStore)
        data_lake_store.name = 'datalakestore-name'
        data_lake_store.set_id('datalakestore_id')
        data_lake_store.with_aliases(data_lake_store.get_id())
        data_lake_store.monitor_diagnostic_settings = [monitor_diagnostic_settings] if monitor_diagnostic_settings else []

        context = AzureEnvironmentContext(data_lake_store=AliasesDict(data_lake_store),
                                          monitor_diagnostic_settings=AliasesDict(*data_lake_store.monitor_diagnostic_settings.copy()))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
