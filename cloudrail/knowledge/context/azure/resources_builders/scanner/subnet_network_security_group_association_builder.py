from typing import List

from cloudrail.knowledge.context.azure.resources.network.azure_security_group_to_subnet_association import AzureSecurityGroupToSubnetAssociation
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SecurityGroupToSubnetAssociationBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'network-security-groups.json'

    def do_build(self, attributes: dict) -> List[AzureSecurityGroupToSubnetAssociation]:
        associations = []
        for subnet_section in attributes['properties'].get('subnets', []):
            associations.append(AzureSecurityGroupToSubnetAssociation(subnet_section['id'], attributes['id']))

        return associations
