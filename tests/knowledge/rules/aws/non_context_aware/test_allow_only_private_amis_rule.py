import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.allow_only_private_amis_rule import AllowOnlyPrivateAmisRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAllowOnlyPrivateAmisRule(unittest.TestCase):
    def setUp(self):
        self.rule = AllowOnlyPrivateAmisRule()

    def test_non_car_ec2_amis_private_only_fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        image_data: Ec2Image = create_empty_entity(Ec2Image)
        image_data.is_public = True
        ec2.image_id = 'image_id'
        ec2.image_data = image_data
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ec2_amis_private_only_pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        image_data: Ec2Image = create_empty_entity(Ec2Image)
        image_data.is_public = False
        ec2.image_id = 'image_id'
        ec2.image_data = image_data
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_ec2_amis_private_only__no_image_data__pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.image_id = 'image_id'
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
