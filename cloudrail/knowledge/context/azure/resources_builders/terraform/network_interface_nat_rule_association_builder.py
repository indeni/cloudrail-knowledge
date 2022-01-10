from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_nat_rule_association import AzureNetworkInterfaceNatRuleAssociation
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class NetworkInterfaceNatRuleAssociationBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkInterfaceNatRuleAssociation:
        return AzureNetworkInterfaceNatRuleAssociation(ip_configuration_name=attributes['ip_configuration_name'],
                                                       network_interface_id=attributes['network_interface_id'],
                                                       nat_rule_id=attributes['nat_rule_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_INTERFACE_NAT_RULE_ASSOCIATION
