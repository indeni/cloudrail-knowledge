import ipaddress

from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import _get_known_value

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_virtual_network import AzureVirtualNetwork
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VirtualNetworkBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        return AzureVirtualNetwork(network_name=attributes['name'],
                                   cidr_addresses=[ipaddress.ip_network(cidr) for cidr in attributes['address_space']],
                                   bgp_community=attributes.get('bgp_community'),
                                   dns_servers=_get_known_value(attributes, 'dns_servers', []),
                                   flow_timeout_in_minutes=int(attributes.get('flow_timeout_in_minutes', -1)))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_NETWORK
