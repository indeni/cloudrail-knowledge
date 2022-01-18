from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterPodSecurityPolicyEnabledRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_gke_ensure_pod_security_policy_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for container_cluster in env_context.container_clusters:
            if not container_cluster.pod_security_policy_enabled:
                issues.append(
                    Issue(
                        f"The {container_cluster.get_type()} `{container_cluster.get_friendly_name()}` has pod security policy disabled",
                        container_cluster,
                        container_cluster))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_clusters)
