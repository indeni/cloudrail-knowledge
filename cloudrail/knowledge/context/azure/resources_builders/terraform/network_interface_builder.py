from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface, IpConfiguration
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class NetworkInterfaceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureNetworkInterface:
        return AzureNetworkInterface(
            name=attributes['name'],
            ip_configurations=[
                IpConfiguration(ip_config['public_ip_address_id'], ip_config['subnet_id'], self._get_known_value(attributes, 'private_ip_address'), [])
                for ip_config in attributes['ip_configuration']])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_NETWORK_INTERFACE
