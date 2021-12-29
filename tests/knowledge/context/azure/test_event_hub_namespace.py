from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet, EventHubNetworkRuleAction, \
    EventHubNetworkRuleNetworkRule
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import ManagedIdentityType
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestEventHubNamespace(AzureContextTest):

    def get_component(self):
        return "event_hub_namespace"

    @context(module_path="default_settings")
    def test_default_settings(self, ctx: AzureEnvironmentContext):
        event_hub_namespace: AzureEventHubNamespace = ctx.event_hub_namespaces.get('/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/'
                                                                                   'resourceGroups/cr3684-rg/providers/Microsoft.EventHub/namespaces/'
                                                                                   'cr3684-eventhubnam')
        self.assertIsNotNone(event_hub_namespace)
        self.assertFalse(event_hub_namespace.auto_inflate_enabled)
        self.assertEqual(event_hub_namespace.capacity, 1)
        self.assertEqual(event_hub_namespace.maximum_throughput_units, 0)
        self.assertEqual(event_hub_namespace.sku, EventHubNamespaceSku.STANDARD)
        self.assertEqual(len(event_hub_namespace.get_monitor_settings()), 0)
        self.assertIsNotNone(event_hub_namespace.network_rule_set)
        net_rule: EventHubNetworkRuleSet = event_hub_namespace.network_rule_set
        self.assertEqual(net_rule.default_action, EventHubNetworkRuleAction.DENY)
        self.assertEqual(net_rule.rule_set_name, 'default')
        self.assertEqual(net_rule.get_id().lower(), '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3684-rg/providers/'
                                                    'Microsoft.EventHub/namespaces/cr3684-eventhubnam/networkRuleSets/default'.lower())
        self.assertEqual(net_rule.ip_mask_list, [])
        self.assertFalse(net_rule.trusted_service_access_enabled)
        self.assertEqual(net_rule.virtual_network_rule_list, [])
        self.assertEqual(len(event_hub_namespace.managed_identities), 0)

    @context(module_path="custom_config")
    def test_custom_config(self, ctx: AzureEnvironmentContext):
        event_hub_namespace: AzureEventHubNamespace = ctx.event_hub_namespaces.get('/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/'
                                                                                   'resourceGroups/cr3684-rg/providers/Microsoft.EventHub/namespaces/'
                                                                                   'cr3684-eventhubnam')
        self.assertIsNotNone(event_hub_namespace)
        self.assertTrue(event_hub_namespace.auto_inflate_enabled)
        self.assertEqual(event_hub_namespace.capacity, 2)
        self.assertEqual(event_hub_namespace.maximum_throughput_units, 2)
        self.assertEqual(event_hub_namespace.sku, EventHubNamespaceSku.STANDARD)
        self.assertEqual(len(event_hub_namespace.get_monitor_settings()), 1)
        self.assertIsNotNone(event_hub_namespace.network_rule_set)
        net_rule: EventHubNetworkRuleSet = event_hub_namespace.network_rule_set
        self.assertEqual(net_rule.default_action, EventHubNetworkRuleAction.DENY)
        self.assertEqual(net_rule.rule_set_name, 'default')
        self.assertEqual(net_rule.get_id().lower(), '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3684-rg/providers/'
                                                    'Microsoft.EventHub/namespaces/cr3684-eventhubnam/networkRuleSets/default'.lower())
        self.assertEqual(net_rule.ip_mask_list, ['10.0.1.0/24'])
        self.assertTrue(net_rule.trusted_service_access_enabled)
        self.assertEqual(len(net_rule.virtual_network_rule_list), 1)
        rule: EventHubNetworkRuleNetworkRule = net_rule.virtual_network_rule_list[0]
        self.assertTrue(rule.ignore_missing_virtual_network_service_endpoint)
        self.assertEqual(rule.subnet_id, '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourcegroups/cr3684-rg/providers/Microsoft.Network/'
                                         'virtualNetworks/cr3684-vnet/subnets/cr3684-subnet')

        self.assertEqual(len(event_hub_namespace.managed_identities), 1)
        self.assertEqual(event_hub_namespace.managed_identities[0].identity_type, ManagedIdentityType.SYSTEM_ASSIGNED)
