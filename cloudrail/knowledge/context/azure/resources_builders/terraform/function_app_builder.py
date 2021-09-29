from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class FunctionAppBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        client_cert_mode: FieldMode = None
        if self._is_known_value(attributes, 'client_cert_mode'):
            client_cert_mode = FieldMode(attributes['client_cert_mode'])

        return AzureFunctionApp(name=attributes['name'],
                                client_cert_mode=client_cert_mode,
                                https_only=self._get_known_value(attributes, 'https_only', False))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_FUNCTION_APP
