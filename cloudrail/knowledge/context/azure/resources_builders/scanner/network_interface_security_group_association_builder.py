from typing import List

from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_security_group_association import \
    AzureNetworkInterfaceSecurityGroupAssociation
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AzureNetworkInterfaceSecurityGroupAssociationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'network-security-groups.json'

    def do_build(self, attributes: dict) -> List[AzureNetworkInterfaceSecurityGroupAssociation]:
        associations = []
        for network_interface_section in attributes['properties'].get('networkInterfaces', []):
            associations.append(AzureNetworkInterfaceSecurityGroupAssociation(network_interface_section['id'], attributes['id']))

        return associations
