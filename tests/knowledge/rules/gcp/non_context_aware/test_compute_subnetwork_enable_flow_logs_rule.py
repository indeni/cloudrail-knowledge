from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork, GcpComputeSubNetworkLogConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_subnetwork_enable_flow_logs_rule import ComputeSubNetworkEnableFlowLogsRule


class TestComputeSubNetworkEnableFlowLogsRule(TestCase):
    def setUp(self):
        self.rule = ComputeSubNetworkEnableFlowLogsRule()

    @parameterized.expand(
        [
            ["Both with flow logs", 0, RuleResultType.SUCCESS],
            ["Both with flow logs", 1, RuleResultType.FAILED],
            ["Without flow logs", 2, RuleResultType.FAILED],
        ]
    )

    def test_compute_subnetwork_enable_flow_log_rule(self, unused_name: str, total_issues: int, rule_status: RuleResultType):
        # Arrange
        compute_subnetworks: AliasesDict[GcpComputeSubNetwork] = AliasesDict()
        log_config_counter = 2 - total_issues
        for i in range(2):
            compute_subnetwork = create_empty_entity(GcpComputeSubNetwork)
            if log_config_counter:
                compute_subnetwork.log_config = create_empty_entity(GcpComputeSubNetworkLogConfig)
                log_config_counter -= 1
            compute_subnetworks.update(compute_subnetwork)

        context = GcpEnvironmentContext(compute_subnetworks=compute_subnetworks)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
