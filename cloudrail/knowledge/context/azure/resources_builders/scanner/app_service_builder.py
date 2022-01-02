from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_scanner_user_managed_identities_ids, \
    create_scanner_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AppServiceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureAppService:
        if attributes['kind'] == AzureAppServiceType.APP.value:
            app_service: AzureAppService = AzureAppService(name=attributes['name'],
                                                           https_only=attributes['properties']['httpsOnly'],
                                                           client_cert_required=attributes['properties'].get('clientCertEnabled', False),
                                                           identities_ids=get_scanner_user_managed_identities_ids(attributes))
            if managed_identity := create_scanner_system_managed_identity(attributes):
                app_service.managed_identities.append(managed_identity)
            return app_service
        return None
