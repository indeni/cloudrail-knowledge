import unittest

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_local_infile_flag_off import SqlDatabaseLocalInfileRule
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import AppServicesDefenderEnabledRule


class TestSqlDatabaseLocalInfileFlagRule(unittest.TestCase):
    def setUp(self):
        self.rule = SqlDatabaseLocalInfileRule()

    @parameterized.expand(
        [
            ['Local-Infile-One-Off-ShouldAlert', SubscriptionPricingResourceType.APP_SERVICES, SubscriptionPricingTier.FREE, True],
            ['Local-Infile-None-Off-ShouldAlert-Ok', SubscriptionPricingResourceType.APP_SERVICES, SubscriptionPricingTier.STANDARD, False],
            ['Local-Infile-Both-Off-ShouldAlert-ShouldAlert', SubscriptionPricingResourceType.DNS, SubscriptionPricingTier.STANDARD, True],
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

    def test_ssl_required(self):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        sql.require_ssl = True
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_ssl_not_required(self):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        sql.require_ssl = False
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
