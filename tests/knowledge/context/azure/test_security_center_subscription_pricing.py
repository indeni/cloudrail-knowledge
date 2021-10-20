from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import SubscriptionPricingResourceType, \
    SubscriptionPricingTier

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSecurityCenterSubscriptionPricing(AzureContextTest):

    def get_component(self):
        return "security_center_subscription_pricing"

    @context(module_path="defender_for_container_registry_enabled")
    def test_defender_for_container_registry_enabled(self, ctx: AzureEnvironmentContext):
        subscription_pricing = self._get_subscription_pricing(ctx)
        self.assertEqual(subscription_pricing.tier, SubscriptionPricingTier.STANDARD)

    @context(module_path="defender_for_container_registry_disabled")
    def test_defender_for_container_registry_disabled(self, ctx: AzureEnvironmentContext):
        subscription_pricing = self._get_subscription_pricing(ctx)
        self.assertEqual(subscription_pricing.tier, SubscriptionPricingTier.FREE)

    def _get_subscription_pricing(self, ctx: AzureEnvironmentContext):
        subscription_pricing = next((sub_pricing for sub_pricing in ctx.security_center_subscription_pricings
                                     if sub_pricing.resource_type == SubscriptionPricingResourceType.CONTAINER_REGISTRY), None)
        self.assertIsNotNone(subscription_pricing)
        return subscription_pricing
