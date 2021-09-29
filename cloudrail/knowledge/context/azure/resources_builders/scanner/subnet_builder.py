from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet


class SubnetsBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'subnets.json'

    def do_build(self, attributes: dict) -> AzureSubnet:
        return AzureSubnet(name=attributes['name'])
