from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_application_security_group_association import AzureNetworkInterfaceApplicationSecurityGroupAssociation

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AzureNetworkInterfaceApplicationSecurityGroupAssociationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkInterfaceApplicationSecurityGroupAssociation:
        return AzureNetworkInterfaceApplicationSecurityGroupAssociation(network_interface_id=attributes['network_interface_id'],
                                                                        application_security_group_id=attributes['application_security_group_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_INTERFACE_APPLICATION_SECURITY_GROUP_ASSOCIATION
