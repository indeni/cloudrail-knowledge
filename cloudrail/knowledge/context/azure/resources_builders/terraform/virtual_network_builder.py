import ipaddress
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_virtual_network import AzureVirtualNetwork
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VirtualNetworkBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        return AzureVirtualNetwork(network_name=attributes['name'],
                                   cidr_addresses=[ipaddress.ip_network(cidr) for cidr in attributes['address_space']])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_NETWORK
