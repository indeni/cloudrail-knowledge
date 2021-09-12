from cloudrail.knowledge.context.azure.resources.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.azure.resources.webapp.constants import FtpsState
from cloudrail.knowledge.context.azure.resources.webapp.diagnostic_logs import DiagnosticLogs

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AppServiceConfigBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service-config.json'

    def do_build(self, attributes: dict) -> AzureAppServiceConfig:
        detailed_error_logging_enabled = attributes['properties'].get('detailedErrorLoggingEnabled', False)
        http_logging_enabled = attributes['properties'].get('httpLoggingEnabled', False)
        request_tracing_enabled = attributes['properties'].get('requestTracingEnabled', False)
        linux_fx_version = attributes['properties'].get('linuxFxVersion')
        java_version = attributes['properties'].get('javaVersion')
        return AzureAppServiceConfig(name=attributes['name'],
                                     ftps_state=FtpsState(attributes['properties']['ftpsState']),
                                     auth_settings=AuthSettings(attributes['properties']['siteAuthEnabled']),
                                     minimum_tls_version=attributes['properties']['minTlsVersion'],
                                     http2_enabled=attributes['properties']['http20Enabled'],
                                     logs=DiagnosticLogs(detailed_error_logging_enabled,
                                                         http_logging_enabled,
                                                         request_tracing_enabled),
                                     linux_fx_version=linux_fx_version,
                                     java_version=java_version)
