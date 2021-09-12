from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_security_group_association import \
    AzureNetworkInterfaceSecurityGroupAssociation

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AzureNetworkInterfaceSecurityGroupAssociationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkInterfaceSecurityGroupAssociation:
        return AzureNetworkInterfaceSecurityGroupAssociation(network_interface_id=attributes['network_interface_id'],
                                                         network_security_group_id=attributes['network_security_group_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_INTERFACE_SECURITY_GROUP_ASSOCIATION
