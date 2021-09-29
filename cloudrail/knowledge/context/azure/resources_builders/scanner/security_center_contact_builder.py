from cloudrail.knowledge.context.azure.resources.security.azure_security_center_contact import AzureSecurityCenterContact

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SecurityCenterContactBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return  'subscription-securityContacts-settings.json'

    def do_build(self, attributes: dict) -> AzureSecurityCenterContact:
        return AzureSecurityCenterContact(alert_notifications=attributes['properties']['alertNotifications']['state'] == 'On')\
            .with_aliases(self.subscription_id)
