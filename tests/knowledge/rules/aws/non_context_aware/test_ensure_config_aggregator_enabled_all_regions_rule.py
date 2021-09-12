import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.configservice.config_aggregator import ConfigAggregator
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_config_aggregator_enabled_all_regions_rule import \
    EnsureConfigAggregatorEnabledAllRegionsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureConfigAggregatorEnabledAllRegionsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureConfigAggregatorEnabledAllRegionsRule()

    def test_non_car_config_aggregator_is_enabled_in_all_regions__account__fail(self):
        # Arrange
        aggregator: ConfigAggregator = create_empty_entity(ConfigAggregator)
        aggregator.account_aggregation_used = True
        aggregator.account_aggregation_all_regions_enabled = False
        context = AwsEnvironmentContext(aws_config_aggregators=[aggregator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_config_aggregator_is_enabled_in_all_regions__organization__fail(self):
        # Arrange
        aggregator: ConfigAggregator = create_empty_entity(ConfigAggregator)
        aggregator.organization_aggregation_used = True
        aggregator.organization_aggregation_all_regions_enabled = False
        context = AwsEnvironmentContext(aws_config_aggregators=[aggregator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_config_aggregator_is_enabled_in_all_regions__account__pass(self):
        # Arrange
        aggregator: ConfigAggregator = create_empty_entity(ConfigAggregator)
        aggregator.account_aggregation_used = True
        aggregator.account_aggregation_all_regions_enabled = True
        context = AwsEnvironmentContext(aws_config_aggregators=[aggregator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_config_aggregator_is_enabled_in_all_regions__organization__pass(self):
        # Arrange
        aggregator: ConfigAggregator = create_empty_entity(ConfigAggregator)
        aggregator.organization_aggregation_used = True
        aggregator.organization_aggregation_all_regions_enabled = True
        context = AwsEnvironmentContext(aws_config_aggregators=[aggregator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
