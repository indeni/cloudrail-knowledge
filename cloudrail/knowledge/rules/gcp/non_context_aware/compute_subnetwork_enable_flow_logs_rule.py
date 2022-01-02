from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ComputeSubNetworkEnableFlowLogsRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_compute_subnetwork_ensure_vpc_flow_logs_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for subnetwork in env_context.compute_subnetworks:
            if subnetwork.name != 'default' and not subnetwork.log_config.enabled:
                issues.append(
                    Issue(
                        f"The {subnetwork.get_type()} `{subnetwork.get_friendly_name()}` does not have flow logs enabled.",
                        subnetwork,
                        subnetwork))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_subnetworks)
