import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_ec2_instance_detailed_monitoring_enabled_rule import \
    EnsureEc2InstanceDetailedMonitoringEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureEc2InstanceDetailedMonitoringEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEc2InstanceDetailedMonitoringEnabledRule()

    def test_non_car_ec2_instance_detailed_monitoring_enabled_fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.monitoring_enabled = False
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ec2_instance_detailed_monitoring_enabled_pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.monitoring_enabled = True
        context = AwsEnvironmentContext(ec2s=[ec2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
