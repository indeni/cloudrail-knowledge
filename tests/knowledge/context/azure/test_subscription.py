from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureNoCloudAccountContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSubscription(AzureNoCloudAccountContextTest):

    def get_component(self):
        return 'subscription'

    # CR-3703 Unable to create new subscription using IaC (Error when apply - Alias methot is not supported)
    @context(module_path="basic", test_options=TestOptions(run_drift_detection=False))
    def test_basic(self, ctx: AzureEnvironmentContext):
        subscription = next((subscription for subscription in ctx.subscriptions if subscription.subscription_name == 'dev_alon'), None)
        self.assertIsNotNone(subscription)
        self.assertEqual(subscription.subscription_id, '00000000-0000-0000-0000-000000000000')
        self.assertEqual(len(subscription.monitor_activity_alert_log_list), 2)
        if subscription.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(subscription._id, 'azurerm_subscription.test.id')
        elif subscription.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(subscription._id, '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a')