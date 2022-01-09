from typing import List
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_nat_rule_association import AzureNetworkInterfaceNatRuleAssociation
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class NetworkInterfaceNatRuleAssociationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'network-interfaces.json'

    def do_build(self, attributes: dict) -> List[AzureNetworkInterfaceNatRuleAssociation]:
        nic_nat_rule_associations = []
        properties = attributes['properties']
        for ip_config in properties.get('ipConfigurations', {}):
            ip_config_name = ip_config['name']
            for nat_rule in ip_config['properties'].get('loadBalancerInboundNatRules', []):
                nic_nat_rule_associations.append(AzureNetworkInterfaceNatRuleAssociation(ip_configuration_name=ip_config_name,
                                                                                         network_interface_id=attributes['id'],
                                                                                         nat_rule_id=nat_rule['id']))
        return nic_nat_rule_associations
