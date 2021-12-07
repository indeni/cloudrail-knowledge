from cloudrail.knowledge.context.azure.resources.webapp.azure_identity import Identity
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AppServiceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        client_cert_required = self._get_known_value(attributes, 'client_cert_enabled', False)
        identity = None
        if self._is_known_value(attributes, 'identity'):
            identity = Identity(type=self._get_known_value(attributes['identity'][0], 'type'),
                                identity_ids=self._get_known_value(attributes['identity'][0], 'identity_ids'))
        return AzureAppService(name=attributes['name'],
                               https_only=self._get_known_value(attributes, 'https_only', False),
                               client_cert_required=client_cert_required, identity=identity)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_APP_SERVICE
