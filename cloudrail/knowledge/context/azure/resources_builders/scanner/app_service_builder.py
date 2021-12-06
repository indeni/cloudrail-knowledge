from cloudrail.knowledge.context.azure.resources.webapp.azure_Identity import Identity
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AppServiceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureAppService:
        if attributes['kind'] == AzureAppServiceType.APP.value:
            identity = get_identity(attributes)
            return AzureAppService(name=attributes['name'],
                                   https_only=attributes['properties']['httpsOnly'],
                                   client_cert_required=attributes['properties'].get('clientCertEnabled', False),
                                   identity=identity)
        return None


def get_identity(attributes):
    identity = None
    if attributes.get('identity'):
        identity_ids = []
        if attributes['identity'].get('type') == 'UserAssigned':
            identity_ids = attributes['identity'].get('userAssignedIdentities')
        elif attributes['identity'].get('type') == 'SystemAssigned':
            if attributes['identity'].get('tenantId'):
                identity_ids.append(attributes['identity'].get('tenantId'))
            if attributes['identity'].get('principalId'):
                identity_ids.append(attributes['identity'].get('principalId'))
        identity = Identity(type=attributes['identity'].get('type'),
                            identity_ids=identity_ids)
    return identity
