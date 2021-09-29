from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup

from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import NetworkSecurityRuleTemplate, create_network_security_rules
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class NetworkSecurityGroupBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkSecurityGroup:
        rules = self._get_known_value(attributes, 'security_rule', [])
        rule_templates = [NetworkSecurityRuleTemplate(nsg_name=attributes['name'],
                                                      rule_name=rule['name'],
                                                      priority=rule['priority'],
                                                      acccess=rule['access'],
                                                      protocol=rule['protocol'],
                                                      direction=rule['direction'],
                                                      destination_port_range=rule['destination_port_range'],
                                                      destination_port_ranges=rule['destination_port_ranges'],
                                                      source_address_prefix=rule['source_address_prefix'],
                                                      source_address_prefixes=rule['source_address_prefixes'],
                                                      destination_address_prefix=rule['destination_address_prefix'],
                                                      destination_address_prefixes=rule['destination_address_prefixes'],
                                                      source_application_security_group_ids=self._get_known_value(attributes, 'source_application_security_group_ids', []),
                                                      destination_application_security_group_ids=self._get_known_value(attributes, 'destination_application_security_group_ids', [])
                                                      ) for rule in rules]
        return AzureNetworkSecurityGroup(name=attributes['name'],
                                         network_security_rules=create_network_security_rules(rule_templates) + self._create_default_rules(attributes['name']))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP

    @staticmethod
    def _create_default_rules(nsg_name: str):
        """
        Creating the default network security rules that are generated automatically with each network securitty group created.
        https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview#default-security-rules
        """
        template1 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='AllowVnetInBound',
            priority=65000,
            acccess='Allow',
            protocol='*',
            direction='Inbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='VirtualNetwork',
            source_address_prefixes=[],
            destination_address_prefix='VirtualNetwork',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        template2 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='AllowAzureLoadBalancerInBound',
            priority=65001,
            acccess='Allow',
            protocol='*',
            direction='Inbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='AzureLoadBalancer',
            source_address_prefixes=[],
            destination_address_prefix='*',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        template3 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='DenyAllInBound',
            priority=65500,
            acccess='Deny',
            protocol='*',
            direction='Inbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='*',
            source_address_prefixes=[],
            destination_address_prefix='*',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        template4 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='AllowVnetOutBound',
            priority=65000,
            acccess='Allow',
            protocol='*',
            direction='Outbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='VirtualNetwork',
            source_address_prefixes=[],
            destination_address_prefix='VirtualNetwork',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        template5 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='AllowInternetOutBound',
            priority=65001,
            acccess='Allow',
            protocol='*',
            direction='Outbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='Internet',
            source_address_prefixes=[],
            destination_address_prefix='*',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        template6 = NetworkSecurityRuleTemplate(
            nsg_name=nsg_name,
            rule_name='DenyAllOutBound',
            priority=65500,
            acccess='Deny',
            protocol='*',
            direction='Outbound',
            destination_port_range='*',
            destination_port_ranges=[],
            source_address_prefix='*',
            source_address_prefixes=[],
            destination_address_prefix='*',
            destination_address_prefixes=[],
            source_application_security_group_ids=[],
            destination_application_security_group_ids=[]
        )

        return create_network_security_rules([template1, template2, template3, template4, template5, template6])
