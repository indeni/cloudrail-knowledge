from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_contact import AzureSecurityCenterContact

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SecurityCenterContactBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSecurityCenterContact:
        return AzureSecurityCenterContact(attributes['alert_notifications']).with_aliases(attributes['subscription_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SECURITY_CENTER_CONTACT
