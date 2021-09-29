from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup

from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import NetworkSecurityRuleTemplate, create_network_security_rules
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class NetworkSecurityGroupBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'network-security-groups.json'

    def do_build(self, attributes: dict) -> AzureNetworkSecurityGroup:
        properties = attributes['properties']
        rule_templates = [NetworkSecurityRuleTemplate(nsg_name=attributes['name'],
                                                      rule_name=rule['name'],
                                                      priority=(rule_properties := rule['properties'])['priority'],
                                                      acccess=rule_properties['access'],
                                                      protocol=rule_properties['protocol'],
                                                      direction=rule_properties['direction'],
                                                      destination_port_range=rule_properties['destinationPortRange'],
                                                      destination_port_ranges=rule_properties['destinationPortRanges'],
                                                      source_address_prefix=rule_properties['sourceAddressPrefix'],
                                                      source_address_prefixes=rule_properties['sourceAddressPrefixes'],
                                                      destination_address_prefix=rule_properties['destinationAddressPrefix'],
                                                      destination_address_prefixes=rule_properties['destinationAddressPrefixes'],
                                                      source_application_security_group_ids=rule_properties.get('sourceApplicationSecurityGroups', []),
                                                      destination_application_security_group_ids=rule_properties.get('destinationApplicationSecurityGroups', []),
                                                      ) for rule in properties['securityRules'] + properties['defaultSecurityRules']]

        return AzureNetworkSecurityGroup(name=attributes['name'],
                                         network_security_rules=create_network_security_rules(rule_templates))
