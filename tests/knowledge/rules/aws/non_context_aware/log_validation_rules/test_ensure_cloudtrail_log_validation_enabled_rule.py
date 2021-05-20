import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_log_validation_enabled_rule import \
    EnsureCloudTrailLogValidationEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudTrailLogValidationEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudTrailLogValidationEnabledRule()

    def test_non_car_aws_cloudtrail_log_validation_disabled_fail(self):
        # Arrange
        trail: CloudTrail = create_empty_entity(CloudTrail)
        trail.log_file_validation = False
        context = EnvironmentContext(cloudtrail=[trail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_aws_cloudtrail_log_validation_disabled_pass(self):
        # Arrange
        trail: CloudTrail = create_empty_entity(CloudTrail)
        trail.log_file_validation = True
        context = EnvironmentContext(cloudtrail=[trail])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
