import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import LaunchConfiguration
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_imdsv2_is_used_rule import EnsureImdsv2IsUsedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureImdsv2IsUsedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureImdsv2IsUsedRule()

    def test_non_car_ensure_imdsv2_fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        launch_config: LaunchConfiguration = create_empty_entity(LaunchConfiguration)
        launch_template: LaunchTemplate = create_empty_entity(LaunchTemplate)
        ec2.http_tokens = 'disabled'
        launch_config.http_tokens = 'disabled'
        launch_template.http_token = 'disabled'
        context = AwsEnvironmentContext(ec2s=[ec2], launch_configurations=[launch_config], launch_templates=[launch_template])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(3, len(result.issues))

    def test_non_car_ensure_imdsv2_pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        launch_config: LaunchConfiguration = create_empty_entity(LaunchConfiguration)
        launch_template: LaunchTemplate = create_empty_entity(LaunchTemplate)
        ec2.http_tokens = 'required'
        launch_config.http_tokens = 'required'
        launch_template.http_token = 'required'
        context = AwsEnvironmentContext(ec2s=[ec2], launch_configurations=[launch_config], launch_templates=[launch_template])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
