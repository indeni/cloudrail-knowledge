from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules, BypassTrafficType, NetworkRuleDefaultAction
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class StorageAccountBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureStorageAccount:
        storage_account = AzureStorageAccount(storage_name=attributes['name'],
                                              account_tier=attributes['account_tier'],
                                              account_replication_type=attributes['account_replication_type'],
                                              enable_https_traffic_only=self._get_known_value(attributes, 'enable_https_traffic_only', True),
                                              allow_blob_public_access=attributes['allow_blob_public_access'])
        if network_rules := self._get_known_value(attributes, 'network_rules'):
            bypass_traffic = [BypassTrafficType.AZURESERVICES]
            if bypass_data := self._get_known_value(network_rules[0], 'bypass'):
                bypass_traffic = []
                for item in bypass_data:
                    bypass_traffic.append(BypassTrafficType(item))
            storage_account.network_rules = AzureStorageAccountNetworkRules(storage_name=attributes['name'],
                                                                            default_action=NetworkRuleDefaultAction(network_rules[0]['default_action'].lower()),
                                                                            ip_rules=self._get_known_value(network_rules[0], 'ip_rules', []),
                                                                            bypass_traffic=bypass_traffic)
        return storage_account

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_STORAGE_ACCOUNT
