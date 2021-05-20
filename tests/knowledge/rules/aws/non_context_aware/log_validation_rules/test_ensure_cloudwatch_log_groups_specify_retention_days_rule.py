import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudwatch_log_groups_specify_retention_days_rule import \
    EnsureCloudWatchLogGroupsRetentionUsageRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudWatchLogGroupsRetentionUsageRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudWatchLogGroupsRetentionUsageRule()

    def test_non_car_cw_log_group_no_retention_fail(self):
        # Arrange
        cloud_watch_log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        cloud_watch_log_group.retention_in_days = False
        context = EnvironmentContext(cloud_watch_log_groups=[cloud_watch_log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cw_log_group_no_retention_pass(self):
        # Arrange
        cloud_watch_log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        cloud_watch_log_group.retention_in_days = True
        context = EnvironmentContext(cloud_watch_log_groups=[cloud_watch_log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
