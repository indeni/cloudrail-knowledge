from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import AzureNetworkSecurityRule

from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import NetworkSecurityRuleTemplate, create_network_security_rules
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class NetworkSecurityGroupRuleBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkSecurityRule:
        rule = create_network_security_rules([NetworkSecurityRuleTemplate(nsg_name=attributes['network_security_group_name'],
                                                                          rule_name=attributes['name'],
                                                                          priority=attributes['priority'],
                                                                          acccess=attributes['access'],
                                                                          protocol=attributes['protocol'],
                                                                          direction=attributes['direction'],
                                                                          destination_port_range=attributes['destination_port_range'],
                                                                          destination_port_ranges=attributes['destination_port_ranges'],
                                                                          source_address_prefix=attributes['source_address_prefix'],
                                                                          source_address_prefixes=attributes['source_address_prefixes'],
                                                                          destination_address_prefix=attributes['destination_address_prefix'],
                                                                          destination_address_prefixes=attributes['destination_address_prefixes'],
                                                                          source_application_security_group_ids=
                                                                          self._get_known_value(attributes, 'source_application_security_group_ids',
                                                                                                []),
                                                                          destination_application_security_group_ids=
                                                                          self._get_known_value(attributes,
                                                                                                'destination_application_security_group_ids', []))])[0]
        return rule

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_SECURITY_RULE
