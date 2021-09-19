import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator import GlobalAccelerator
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_attributes import GlobalAcceleratorAttribute
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_global_acceleration_flow_logs_enabled_rule import \
    EnsureGlobalAccelerationFlowLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureGlobalAccelerationFlowLogsEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureGlobalAccelerationFlowLogsEnabledRule()

    def test_non_car_global_accelerator_flow_logs_enabled_fail(self):
        # Arrange
        global_accelerator: GlobalAccelerator = create_empty_entity(GlobalAccelerator)
        global_accelerator_attributes: GlobalAcceleratorAttribute = create_empty_entity(GlobalAcceleratorAttribute)
        global_accelerator_attributes.flow_logs_enabled = False
        global_accelerator.attributes = global_accelerator_attributes
        context = AwsEnvironmentContext(global_accelerators=[global_accelerator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_global_accelerator_flow_logs_enabled_pass(self):
        # Arrange
        global_accelerator: GlobalAccelerator = create_empty_entity(GlobalAccelerator)
        global_accelerator_attributes: GlobalAcceleratorAttribute = create_empty_entity(GlobalAcceleratorAttribute)
        global_accelerator_attributes.flow_logs_enabled = True
        global_accelerator.attributes = global_accelerator_attributes
        context = AwsEnvironmentContext(global_accelerators=[global_accelerator])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
