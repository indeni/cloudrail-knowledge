from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.app_service_config_builder import AppServiceConfigBuilder


class FunctionAppConfigBuilder(AppServiceConfigBuilder):
    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_FUNCTION_APP  ## since terraform don't have service config entity, we are taking the needed prop from the app service
