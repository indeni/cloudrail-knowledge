from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_security_group_to_subnet_association import \
    AzureSecurityGroupToSubnetAssociation

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SecurityGroupToSubnetAssociationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSecurityGroupToSubnetAssociation:
        return AzureSecurityGroupToSubnetAssociation(subnet_id=attributes['subnet_id'],
                                                     network_security_group_id=attributes['network_security_group_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SUBNET_NETWORK_SECURITY_GROUP_ASSOCIATION
