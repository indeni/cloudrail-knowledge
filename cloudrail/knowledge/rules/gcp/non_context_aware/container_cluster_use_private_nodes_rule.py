from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterUsePrivateNodesRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_gke_ensure_clusters_private_nodes'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for container_cluster in env_context.container_clusters:
            if not container_cluster.private_cluster_config or not container_cluster.private_cluster_config.enable_private_nodes:
                issues.append(
                    Issue(
                        f"The {container_cluster.get_type()} `{container_cluster.get_friendly_name()}` "
                        f"has cluster nodes configured with public ip addresses",
                        container_cluster,
                        container_cluster))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_clusters)
