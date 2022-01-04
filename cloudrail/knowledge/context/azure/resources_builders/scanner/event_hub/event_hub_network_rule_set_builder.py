from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet, EventHubNetworkRuleAction, \
    EventHubNetworkRuleNetworkRule
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class EventHubNetworkRuleSetBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-network-rule-sets.json'

    def do_build(self, attributes: dict) -> EventHubNetworkRuleSet:
        properties: dict = attributes['properties']
        return EventHubNetworkRuleSet(rule_set_id=attributes['id'],
                                      rule_set_name=attributes['name'],
                                      event_hub_namespace_id='/'.join(attributes['id'].split('/')[:-2]),
                                      default_action=EventHubNetworkRuleAction(properties['defaultAction']),
                                      trusted_service_access_enabled=properties.get('trustedServiceAccessEnabled', False),
                                      virtual_network_rule_list=[
                                          EventHubNetworkRuleNetworkRule(subnet_id=net_rule['subnet']['id'],
                                                                         ignore_missing_virtual_network_service_endpoint=net_rule
                                                                         .get('ignoreMissingVnetServiceEndpoint', False))
                                          for net_rule in properties.get('virtualNetworkRules', [])
                                    ],
                                      ip_mask_list=[ip_rule.get('ipMask') for ip_rule in properties.get('ipRules', [])])
