from typing import List, Dict, Optional

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpClusterContainerBinaryAuthorizationPolicy, \
    GcpBinaryAuthorizationAdmissionEvaluationMode
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterUseAuthorizationPolicyRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'car_gke_ensure_binary_authorization'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for cluster in env_context.container_clusters:
            if not cluster.enable_binary_authorization:
                issues.append(
                            Issue(
                                f"The {cluster.get_type()} `{cluster.get_friendly_name()}` has binary authorization disabled",
                                cluster,
                                cluster))
            else:
                if policy := self._get_affected_policy(env_context, cluster):
                    issues.append(
                        Issue(
                            f"The {cluster.get_type()} `{cluster.get_friendly_name()}` has binary authorization enabled but the evaluation mode set to always allow",
                            policy,
                            cluster))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_clusters)

    @staticmethod
    def _get_affected_policy(environment_context: GcpEnvironmentContext,
                             container_cluster: GcpContainerCluster) -> Optional[GcpClusterContainerBinaryAuthorizationPolicy]:
        if any(policy.evaluation_mode == GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_ALLOW
               for policy in container_cluster.binary_auth_policies):
            binary_auth_policy = next((policy for policy in environment_context.binary_authorization_policies
                                       if policy.project_id == container_cluster.project_id), None)
            return binary_auth_policy
        return None
