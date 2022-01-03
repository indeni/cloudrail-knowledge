from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_serial_port_connection_rule import ComputeInstanceNoSerialPortConnectionRule


class TestComputeInstanceNoSerialPortConnectionRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceNoSerialPortConnectionRule()

    @parameterized.expand(
        [
            ["Serial port disabled", {'foo': 'bar'}, False],
            ["Serial port enabled", {'serial-port-enable': 'true'}, True]
        ]
    )

    def test_compute_instance_serial_port_connection(self, unused_name: str, metadata: dict, should_alert: bool):
        # Arrange
        compute_instance = create_empty_entity(GcpComputeInstance)
        compute_instance.metadata = metadata
        context = GcpEnvironmentContext(compute_instances=[compute_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
