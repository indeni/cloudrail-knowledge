from typing import Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet, EventHubNetworkRuleAction, \
    EventHubNetworkRuleNetworkRule
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class EventHubNetworkRuleSetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> Optional[EventHubNetworkRuleSet]:
        network_rule_set: Optional[EventHubNetworkRuleSet] = None
        if rule_set := attributes.get('network_rulesets', []):
            rule_set = rule_set[0]
            rule_set_name: str = 'default'
            network_rule_set = EventHubNetworkRuleSet(rule_set_id='/'.join([attributes['id'], 'networkrulesets', rule_set_name]),
                                                      rule_set_name=rule_set_name,
                                                      event_hub_namespace_id=attributes['id'],
                                                      default_action=EventHubNetworkRuleAction(rule_set['default_action']),
                                                      trusted_service_access_enabled=rule_set.get('trusted_service_access_enabled', False),
                                                      virtual_network_rule_list=[
                                                          EventHubNetworkRuleNetworkRule(subnet_id=net_rule['subnet_id'],
                                                                                         ignore_missing_virtual_network_service_endpoint=net_rule
                                                                                         .get('ignore_missing_virtual_network_service_endpoint',
                                                                                              False))
                                                          for net_rule in rule_set.get('virtual_network_rule', [])],
                                                      ip_mask_list=[ip_rule.get('ip_mask') for ip_rule in rule_set.get('ip_rule', [])])
        return network_rule_set

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_EVENTHUB_NAMESPACE
