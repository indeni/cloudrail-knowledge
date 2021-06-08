import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_all_resources_tagged_rule import EnsureAllResourcesTaggedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureAllResourcesTaggedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAllResourcesTaggedRule()

    def test_non_car_all_resources_tagged_fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        tags = {'name': 'ec2_instance'}
        ec2.tags = tags
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_all_resources_tagged_pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        tags = {'name': 'ec2_instance', 'Env': 'Cloudrail'}
        ec2.tags = tags
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
