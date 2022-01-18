from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterAutoNodeUpgradeEnabledRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'car_gke_ensure_auto_node_upgrade_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for container_cluster in env_context.container_clusters:
            for node in container_cluster.node_pools:
                if not node.management.auto_upgrade:
                    issues.append(
                        Issue(
                            f"The {node.get_type()} `{node.get_friendly_name()}` has automatic node upgrade disabled",
                            container_cluster,
                            node))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_clusters and environment_context.container_node_pools)
