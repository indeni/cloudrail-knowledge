import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_cloudtrail_multiregion_enabled_rule import EnsureCloudtrailMultiregionEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudtrailMultiregionEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudtrailMultiregionEnabledRule()

    def test_non_car_cloudtrail_is_enabled_in_all_regions_fail(self):
        # Arrange
        trail: CloudTrail = create_empty_entity(CloudTrail)
        trail.is_multi_region_trail = False
        context = AwsEnvironmentContext(cloudtrail=[trail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudtrail_is_enabled_in_all_regions_pass(self):
        # Arrange
        trail: CloudTrail = create_empty_entity(CloudTrail)
        trail.is_multi_region_trail = True
        context = AwsEnvironmentContext(cloudtrail=[trail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
