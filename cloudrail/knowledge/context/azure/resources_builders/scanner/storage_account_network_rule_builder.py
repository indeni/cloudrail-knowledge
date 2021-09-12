from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules, BypassTrafficType, NetworkRuleDefaultAction
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class StorageAccountNetworkRuleBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'storage-accounts-list.json'

    def do_build(self, attributes: dict) -> AzureStorageAccountNetworkRules:
        network_rules_data = attributes['properties']['networkAcls']
        ip_rules = network_rules_data['ipRules']
        if ip_rules:
            ip_rules = [rule.get('value') for rule in ip_rules]
        bypass_data = network_rules_data['bypass'].replace(' ', '').split(',')
        if not isinstance(bypass_data, list):
            bypass_traffic = [BypassTrafficType(bypass_data)]
        else:
            bypass_traffic = []
            for item in bypass_data:
                bypass_traffic.append(BypassTrafficType(item))
        return AzureStorageAccountNetworkRules(storage_name=attributes['name'],
                                               default_action=NetworkRuleDefaultAction(network_rules_data['defaultAction'].lower()),
                                               ip_rules=ip_rules,
                                               bypass_traffic=bypass_traffic)
