import unittest

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import AzureSecurityCenterSubscriptionPricing, \
    SubscriptionPricingResourceType, SubscriptionPricingTier
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import SqlServersDefenderEnabledRule


class TestSqlServersDefenderEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = SqlServersDefenderEnabledRule()

    @parameterized.expand(
        [
            ['SqlServers-FreeTier-ShouldAlert', SubscriptionPricingResourceType.SQL_SERVERS, SubscriptionPricingTier.FREE, True],
            ['SqlServers-Standard-Ok', SubscriptionPricingResourceType.SQL_SERVERS, SubscriptionPricingTier.STANDARD, False],
            ['OtherResourceType-Standard-Ok', SubscriptionPricingResourceType.DNS, SubscriptionPricingTier.STANDARD, False],
            ['OtherResourceType-Free-Ok', SubscriptionPricingResourceType.DNS, SubscriptionPricingTier.FREE, False],
        ]
    )
    def test_alert_notifications(self, unused_name: str, resource_type: SubscriptionPricingResourceType, tier: SubscriptionPricingTier, should_alert: bool):
        # Arrange
        subscription_pricing = create_empty_entity(AzureSecurityCenterSubscriptionPricing)
        subscription_pricing.resource_type = resource_type
        subscription_pricing.tier = tier
        context = AzureEnvironmentContext(security_center_subscription_pricings=[subscription_pricing])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
