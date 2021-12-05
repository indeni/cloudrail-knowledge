from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp, Identity
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class FunctionAppBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureFunctionApp:
        if AzureAppServiceType.FUNCTION_APP.value in attributes['kind']:
            identity = None
            client_cert_mode: FieldMode = FieldMode('Required')
            if attributes['properties']['clientCertMode']:
                client_cert_mode = FieldMode(attributes['properties']['clientCertMode'])
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
            return AzureFunctionApp(name=attributes['name'],
                                    client_cert_mode=client_cert_mode,
                                    https_only=attributes['properties']['httpsOnly'],
                                    identity=identity)
        return None
