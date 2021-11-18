from typing import List
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, GcpComputeInstanceNetIntfAccessCfg
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_public_ip_rule import ComputeInstanceNoPublicIpRule


class TestComputeInstanceNoPublicIpRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceNoPublicIpRule()

    @parameterized.expand(
        [
            ["One public ip", ["1.1.1.1"], 1, RuleResultType.FAILED],
            ["Both public ip", ["1.1.1.1", "2.2.2.2"], 2, RuleResultType.FAILED],
            ["No public ip", [], 0, RuleResultType.SUCCESS],
        ]
    )

    def test_compute_instance_public_ip(self, unused_name: str, public_ips: dict, total_issues: int, rule_status: RuleResultType):
        # Arrange
        compute_instances: List[GcpComputeInstance] = []
        for i in range(2):
            compute_instances.append(create_empty_entity(GcpComputeInstance))

        for i, public_ip in enumerate(public_ips):
            compute_instances[i].network_interfaces = [create_empty_entity(GcpComputeInstanceNetworkInterface)]
            compute_instances[i].network_interfaces[0].access_config = [create_empty_entity(GcpComputeInstanceNetIntfAccessCfg)]
            compute_instances[i].network_interfaces[0].access_config[0].nat_ip = public_ip

        context = GcpEnvironmentContext(compute_instances=compute_instances)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
