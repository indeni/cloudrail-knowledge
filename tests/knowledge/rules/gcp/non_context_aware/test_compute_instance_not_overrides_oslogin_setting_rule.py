from typing import List
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, GcpComputeInstanceNetIntfAccessCfg
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_not_overrides_oslogin_setting_rule import ComputeInstanceNotOverridesOsLoginSettingRule


class TestComputeInstanceNotOverridesOsLoginSettingRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceNotOverridesOsLoginSettingRule()

    @parameterized.expand(
        [
            ["Both enable oslogin true", [{'enable-oslogin': 'TRUE'}, {'enable-oslogin': 'TRUE'}], 0, RuleResultType.SUCCESS],
            ["One enable oslogin true second_false", [{'enable-oslogin': 'TRUE'}, {'enable-oslogin': 'FALSE'}], 1, RuleResultType.FAILED],
            ["Without enable oslogin", [{}, {}], 0, RuleResultType.SUCCESS],
        ]
    )

    def test_compute_instance_not_overrides_oslogin_setting(self, unused_name: str, metadata_list: List[dict], total_issues: int, rule_status: RuleResultType):
        # Arrange
        compute_instances: List[GcpComputeInstance] = []
        for metadata in metadata_list:
            compute_instance: GcpComputeInstance = create_empty_entity(GcpComputeInstance)
            compute_instance.metadata = metadata
            compute_instances.append(compute_instance)

        context = GcpEnvironmentContext(compute_instances=compute_instances)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
