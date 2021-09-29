from cloudrail.knowledge.context.azure.resources.network.azure_public_ip import AzurePublicIp

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class PublicIpBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'public-ip-addresses.json'

    def do_build(self, attributes: dict) -> AzurePublicIp:
        return AzurePublicIp(name=attributes['name'],
                             public_ip_address=attributes['properties'].get('ipAddress'))
