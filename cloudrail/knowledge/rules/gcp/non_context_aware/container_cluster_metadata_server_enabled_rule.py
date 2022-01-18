from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerClusterWorkloadMetadataConfigMode
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterMetadataServerEnabledRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_gke_ensure_metadata_server_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for container_cluster in env_context.container_clusters:
            if container_cluster.node_config.workload_metadata_config_mode != GcpContainerClusterWorkloadMetadataConfigMode.GKE_METADATA:
                issues.append(
                    Issue(
                        f"The {container_cluster.get_type()} `{container_cluster.get_friendly_name()}` does not have gke metadata server running",
                        container_cluster,
                        container_cluster))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_clusters)
