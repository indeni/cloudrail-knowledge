from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsRetentionPolicySettings, AzureMonitorDiagnosticLogsSettings

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class MonitorDiagnosticSettingBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureMonitorDiagnosticSetting:
        log_settings = None
        retention_policy = None
        if raw_logs := attributes['log']:
            logs_enabled = raw_logs[0]['enabled']
            if raw_retention_policy := raw_logs[0]['retention_policy']:
                retention_policy = AzureMonitorDiagnosticLogsRetentionPolicySettings(raw_retention_policy[0]['enabled'],
                                                                                     self._get_known_value(raw_retention_policy[0], 'days', 0))
            log_settings = AzureMonitorDiagnosticLogsSettings(logs_enabled, retention_policy)

        target_resource_id = self._get_target_resource_id(attributes)

        return AzureMonitorDiagnosticSetting(name=attributes['name'], target_resource_id=target_resource_id, logs_settings=log_settings)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MONITOR_DIAGNOSTIC_SETTING

    def _get_target_resource_id(self, attributes: dict) -> str:
        if not self._is_known_value(attributes, 'target_resource_id'):
            return attributes['target_resource_id']

        return attributes['target_resource_id'].lower()
