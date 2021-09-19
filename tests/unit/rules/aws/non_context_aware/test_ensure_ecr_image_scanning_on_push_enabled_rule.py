import unittest

from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_image_scanning_on_push_enabled_rule import EnsureEcrImageScanningOnPushEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureEcrImageScanningOnPushEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcrImageScanningOnPushEnabledRule()

    def test_non_car_ecr_image_scanning_on_push_enabled_fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.is_image_scan_on_push = False
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ecr_image_scanning_on_push_enabled_pass(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.is_image_scan_on_push = True
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
