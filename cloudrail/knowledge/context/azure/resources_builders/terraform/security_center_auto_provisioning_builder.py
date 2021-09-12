from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_auto_provisioning import AzureSecurityCenterAutoProvisioning

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SecurityCenterAutoProvisioningBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSecurityCenterAutoProvisioning:
        return AzureSecurityCenterAutoProvisioning(attributes['auto_provision'] == 'On').with_aliases(attributes['subscription_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SECURITY_CENTER_AUTO_PROVISIONING
