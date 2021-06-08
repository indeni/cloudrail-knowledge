import unittest

from cloudrail.knowledge.context.aws.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_repository_image_tags_immutable_rule import EnsureEcrRepositoryImageTagsImmutableRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureEcrRepositoryImageTagsImmutableRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcrRepositoryImageTagsImmutableRule()

    def test_non_car_ecr_image_tags_immutable_rule_fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.image_tag_mutability = 'MUTABLE'
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ecr_image_tags_immutable_rule_pass(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.image_tag_mutability = 'IMMUTABLE'
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
