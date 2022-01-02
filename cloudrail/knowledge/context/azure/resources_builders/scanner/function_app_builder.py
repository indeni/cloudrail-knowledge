from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_scanner_user_managed_identities_ids, \
    create_scanner_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class FunctionAppBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureFunctionApp:
        if AzureAppServiceType.FUNCTION_APP.value in attributes['kind']:
            client_cert_mode: FieldMode = FieldMode('Required')
            func_app: AzureFunctionApp = AzureFunctionApp(name=attributes['name'],
                                                          client_cert_mode=client_cert_mode,
                                                          https_only=attributes['properties']['httpsOnly'],
                                                          identities_ids=get_scanner_user_managed_identities_ids(attributes))
            if managed_identity := create_scanner_system_managed_identity(attributes):
                func_app.managed_identities.append(managed_identity)
            return func_app
        return None
