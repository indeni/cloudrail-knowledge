from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class ApplicationSecurityGroupBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'application-security-groups.json'

    def do_build(self, attributes: dict) -> AzureApplicationSecurityGroup:
        return AzureApplicationSecurityGroup(name=attributes['name'])
