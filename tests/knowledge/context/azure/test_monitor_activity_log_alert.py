from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestMonitorActivityLogAlert(AzureContextTest):

    def get_component(self):
        return "monitor_activity_log_alert"

    @context(module_path="basic")
    def test_monitor_activity_log_administrative(self, ctx: AzureEnvironmentContext):
        monitor = next((monitor for monitor in ctx.monitor_activity_log_alert if monitor.name == 'cr3690-activitylogalert1'), None)
        self.assertIsNotNone(monitor)
        self.assertTrue(monitor.enabled)
        self.assertEqual(monitor.scopes, ['/subscriptions/230613d8-3b34-4790-b650-36f31045f19a'])
        self.assertEqual(monitor.description, 'log alert rule')
        self.assertIsNotNone(monitor.criteria)
        self.assertEqual(monitor.criteria.category.value, 'Administrative')
        self.assertEqual(monitor.criteria.operation_name, 'Microsoft.Network/networkSecurityGroups/write')
        self.assertEqual(monitor.criteria.resource_provider, 'Microsoft.Network')
        self.assertEqual(monitor.criteria.resource_type, 'networkSecurityGroups')
        self.assertEqual(monitor.criteria.resource_group, 'fakename')
        self.assertEqual(monitor.criteria.caller, 'fake@emailaddress.com')
        self.assertEqual(monitor.criteria.level.value, 'Warning')
        self.assertIsNone(monitor.criteria.status)  # None because invalid value in main tf
        self.assertEqual(monitor.criteria.sub_status, 'Failed')
        self.assertEqual(monitor.criteria.recommendation_category.value, 'OperationalExcellence')
        self.assertEqual(monitor.criteria.recommendation_impact.value, 'High')
        self.assertIsNone(monitor.criteria.recommendation_type)
        for action in monitor.actions:
            self.assertEqual(action.webhook_properties, {'key': 'value'})
        self.assertEqual(monitor.tags, {'environment': 'production'})
        self.assertIsNone(monitor.criteria.service_health)

        if monitor.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(monitor.criteria.resource_id, 'azurerm_network_security_group.nsg.id')
            for action in monitor.actions:
                self.assertTrue(action.action_group_id in ['azurerm_monitor_action_group.test.id', 'azurerm_monitor_action_group.test10.id'])
        elif monitor.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(monitor.criteria.resource_id, '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3690-RG/providers/Microsoft.'
                                                           'Network/networkSecurityGroups/cr3690-nsg')
            for action in monitor.actions:
                self.assertTrue(action.action_group_id in ['/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3690-RG/providers/Microsoft.'
                                                                   'Insights/actionGroups/doron_test',
                                                                   '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3690-RG/providers/Microsoft.'
                                                                   'Insights/actionGroups/example-actiongroup'])
