from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_terraform_user_managed_identities_ids, \
    create_terraform_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AppServiceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        client_cert_required = self._get_known_value(attributes, 'client_cert_enabled', False)
        app_service: AzureAppService = AzureAppService(name=attributes['name'],
                                                       https_only=self._get_known_value(attributes, 'https_only', False),
                                                       client_cert_required=client_cert_required,
                                                       identities_ids=get_terraform_user_managed_identities_ids(attributes))

        if managed_identity := create_terraform_system_managed_identity(attributes):
            app_service.managed_identities.append(managed_identity)
        return app_service

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_APP_SERVICE
