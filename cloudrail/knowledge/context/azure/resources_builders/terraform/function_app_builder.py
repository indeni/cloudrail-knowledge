from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_terraform_user_managed_identities_ids, \
    create_terraform_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class FunctionAppBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        client_cert_mode: FieldMode = FieldMode('Required')
        if self._is_known_value(attributes, 'client_cert_mode'):
            client_cert_mode = FieldMode(attributes['client_cert_mode'])
        func_app: AzureFunctionApp = AzureFunctionApp(name=attributes['name'],
                                                      client_cert_mode=client_cert_mode,
                                                      https_only=self._get_known_value(attributes, 'https_only', False),
                                                      identities_ids=get_terraform_user_managed_identities_ids(attributes))
        if managed_identity := create_terraform_system_managed_identity(attributes):
            func_app.managed_identities.append(managed_identity)
        return func_app

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_FUNCTION_APP
