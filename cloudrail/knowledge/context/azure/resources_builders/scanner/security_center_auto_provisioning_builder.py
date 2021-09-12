from cloudrail.knowledge.context.azure.resources.security.azure_security_center_auto_provisioning import AzureSecurityCenterAutoProvisioning

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SecurityCenterAutoProvisioningBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'security-center-auto-provisioning.json'

    def do_build(self, attributes: dict) -> AzureSecurityCenterAutoProvisioning:
        return AzureSecurityCenterAutoProvisioning(auto_provision_is_on=attributes['properties']['autoProvision'] == 'On')\
            .with_aliases(self.subscription_id)
