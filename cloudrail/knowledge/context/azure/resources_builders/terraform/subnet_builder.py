import ipaddress
from typing import List

from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SubnetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSubnet:
        cidr_addresses: List[ipaddress.IPv4Network] = [ipaddress.ip_network(cidr) for cidr in attributes['address_prefixes']]
        return AzureSubnet(name=attributes['name'],
                           network_name=attributes['virtual_network_name'],
                           cidr_addresses=cidr_addresses)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SUBNET
