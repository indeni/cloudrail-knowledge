from typing import Optional
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceServiceAcount
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_ensure_no_ip_forwarding_rule import \
    ComputeInstanceEnsureNoIpForwardingRule


class TestComputeInstanceEnsureNoIpForwardingRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceEnsureNoIpForwardingRule()

    @parameterized.expand(
        [
            ["ip forwarding", True, True],
            ["no ip forwarding", False, False]
        ]
    )

    def test_compute_instance_ensure_no_ip_forwarding(self, unused_name: str, can_ip_forward: bool, should_alert: bool):
        # Arrange
        compute_instance = create_empty_entity(GcpComputeInstance)
        compute_instance.can_ip_forward = can_ip_forward
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
