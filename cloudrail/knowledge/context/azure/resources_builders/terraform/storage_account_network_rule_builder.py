from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules, BypassTrafficType, NetworkRuleDefaultAction
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class StorageAccountNetworkRuleBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureStorageAccountNetworkRules:
        bypass_traffic = [BypassTrafficType.AZURESERVICES]
        if bypass_data := self._get_known_value(attributes, 'bypass'):
            bypass_traffic = []
            for item in bypass_data:
                bypass_traffic.append(BypassTrafficType(item))
        return AzureStorageAccountNetworkRules(storage_name=attributes['storage_account_name'],
                                               default_action=NetworkRuleDefaultAction(attributes['default_action'].lower()),
                                               ip_rules=self._get_known_value(attributes, 'ip_rules', []),
                                               bypass_traffic=bypass_traffic)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_STORAGE_ACCOUNT_NETWORK_RULES
