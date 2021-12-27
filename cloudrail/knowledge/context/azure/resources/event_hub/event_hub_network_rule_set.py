from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class EventHubNetworkRuleAction(Enum):
    ALLOW = 'Allow'
    DENY = 'Deny'


@dataclass
class EventHubNetworkRuleNetworkRule:
    """
        Attributes:
            subnet_id: The ID of the subnet to match on.
            ignore_missing_virtual_network_service_endpoint: Whether to ignore missing virtual network service endpoints.
    """
    subnet_id: str
    ignore_missing_virtual_network_service_endpoint: bool


class EventHubNetworkRuleSet(AzureResource):
    """
        Attributes:
            rule_set_id: network rule set id
            rule_set_name: network rule set name
            event_hub_namespace_id: event hub namespace id
            default_action: The default action to take when a rule is not matched (allowed values: 'Allow' or ' Deny')
            trusted_service_access_enabled: Whether Trusted Microsoft Services are allowed to bypass firewall.
            virtual_network_rule_list: A list of virtual network rules.
            ip_mask_list: A list of IP rules.
    """

    def __init__(self, rule_set_id: str, rule_set_name: str, event_hub_namespace_id: str,
                 default_action: EventHubNetworkRuleAction, trusted_service_access_enabled: bool,
                 virtual_network_rule_list: List[EventHubNetworkRuleNetworkRule], ip_mask_list: List[str]):
        super().__init__(AzureResourceType.AZURERM_EVENTHUB_NAMESPACE)
        self.rule_set_id: str = rule_set_id
        self.rule_set_name: str = rule_set_name or rule_set_id.split('/')[-1]
        self.event_hub_namespace_id: str = event_hub_namespace_id
        self.default_action: EventHubNetworkRuleAction = default_action
        self.trusted_service_access_enabled: bool = trusted_service_access_enabled
        self.virtual_network_rule_list: List[EventHubNetworkRuleNetworkRule] = virtual_network_rule_list
        self.ip_mask_list: List[str] = ip_mask_list
        self.with_aliases(self.event_hub_namespace_id)

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.EventHub/namespaces/{self.event_hub_namespace_id.split("/")[-1]}/networking'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.rule_set_id

    def get_name(self) -> Optional[str]:
        return self.rule_set_name

    def to_drift_detection_object(self) -> dict:
        return {
            'default_action': self.default_action.value,
            'trusted_service_access_enabled': self.trusted_service_access_enabled,
            'virtual_network_rule_list': [asdict(net_rule) for net_rule in self.virtual_network_rule_list],
            'ip_mask_list': self.ip_mask_list
        }
