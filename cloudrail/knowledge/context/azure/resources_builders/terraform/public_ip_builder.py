from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_public_ip import AzurePublicIp

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class PublicIpBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzurePublicIp:
        return AzurePublicIp(name=attributes['name'],
                            public_ip_address=self._get_known_value(attributes, 'ip_address'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_PUBLIC_IP
