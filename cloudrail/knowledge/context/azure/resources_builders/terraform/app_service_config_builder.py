from typing import Optional

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState
from cloudrail.knowledge.context.azure.resources.webapp.diagnostic_logs import DiagnosticLogs
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AppServiceConfigBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureAppServiceConfig:
        ftps_state = FtpsState.ALL_ALLOWED
        min_tls_version = '1.2'
        http2_enabled = False
        linux_fx_version = ''
        java_version = None
        if site_config := self._get_known_value(attributes, 'site_config'):
            if site_config_ftps_state := self._get_known_value(site_config[0], 'ftps_state', ftps_state):
                ftps_state = FtpsState(site_config_ftps_state)
            min_tls_version = self._get_known_value(site_config[0], 'min_tls_version', min_tls_version)
            http2_enabled = self._get_known_value(site_config[0], 'http2_enabled', http2_enabled)
            linux_fx_version = self._get_known_value(site_config[0], 'linux_fx_version', linux_fx_version)
            java_version = self._get_known_value(site_config[0], 'java_version', java_version)

        auth_settings: Optional[AuthSettings] = AuthSettings(False)
        if self._is_known_value(attributes, 'auth_settings'):
            auth_settings_dict: dict = attributes['auth_settings'][0]
            auth_settings = AuthSettings(auth_settings_dict['enabled'])

        logs: Optional[DiagnosticLogs] = DiagnosticLogs(False, False, False)
        if logs_dict := self._get_known_value(attributes, 'logs'):
            logs.detailed_error_logging_enabled = self._get_known_value(logs_dict[0], 'detailed_error_messages_enabled', False)
            logs.request_tracing_enabled = self._get_known_value(logs_dict[0], 'failed_request_tracing_enabled', False)
            http_logs_settings = self._get_known_value(logs_dict[0], 'http_logs')
            logs.http_logging_enabled = bool(http_logs_settings and (http_logs_settings[0]['file_system'] or http_logs_settings[0]['azure_blob_storage']))

        return AzureAppServiceConfig(attributes['name'], ftps_state, auth_settings, min_tls_version, http2_enabled, logs,
                                     linux_fx_version, java_version)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_APP_SERVICE  ## since terraform don't have service config entity, we are taking the needed prop from the app service
