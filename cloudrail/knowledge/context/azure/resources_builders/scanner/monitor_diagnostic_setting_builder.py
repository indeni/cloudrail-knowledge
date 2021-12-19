from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class MonitorDiagnosticSettingBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return '*-diagnostic-settings.json'

    def do_build(self, attributes: dict) -> AzureMonitorDiagnosticSetting:
        # The target resource id is the partial id of the monitoring diagnostic settings, as it is tightly coupled to the target
        target_resource_id = "/".join(attributes['id'].split("/", 9)[:9])
        log_settings = None
        retention_policy = None
        if raw_logs_block := attributes['properties'].get('logs'):
            raw_logs_block = raw_logs_block[0]
            logs_enabled = raw_logs_block['enabled']
            if raw_retention_policy := raw_logs_block.get('retentionPolicy'):
                retention_policy = AzureMonitorDiagnosticLogsRetentionPolicySettings(raw_retention_policy['enabled'], raw_retention_policy['days'])
            log_settings = AzureMonitorDiagnosticLogsSettings(logs_enabled, retention_policy)

        return AzureMonitorDiagnosticSetting(name=attributes['name'], target_resource_id=target_resource_id, logs_settings=log_settings)
