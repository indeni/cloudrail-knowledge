from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class ApplicationSecurityGroupBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureApplicationSecurityGroup:
        return AzureApplicationSecurityGroup(name=attributes['name'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_APPLICATION_SECURITY_GROUP
