from typing import List, Optional
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpClusterContainerBinaryAuthorizationPolicy, \
    GcpBinaryAuthorizationAdmissionRuleType, GcpBinaryAuthorizationAdmissionRule, GcpBinaryAuthorizationAdmissionEvaluationMode, \
    GcpBinaryAuthorizationAdmissionEnforcementMode
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class BinaryAuthorizationPolicyBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpClusterContainerBinaryAuthorizationPolicy:
        cluster_admission_rules: List[GcpBinaryAuthorizationAdmissionRule] = []
        for rule in self._get_known_value(attributes, 'cluster_admission_rules', []):
            cluster_admission_rules.append(self._build_admission_rule(rule, GcpBinaryAuthorizationAdmissionRuleType.CLUSTER, rule['cluster']))
        global_policy_evaluation_mode_enabled = self._get_known_value(attributes, 'global_policy_evaluation_mode') == 'ENABLE'
        return GcpClusterContainerBinaryAuthorizationPolicy(default_admission_rule=self._build_admission_rule(attributes['default_admission_rule'][0],
                                                                                                              GcpBinaryAuthorizationAdmissionRuleType.DEFAULT),
                                                            cluster_admission_rules=cluster_admission_rules,
                                                            global_policy_evaluation_mode_enabled=global_policy_evaluation_mode_enabled)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_BINARY_AUTHORIZATION_POLICY

    @classmethod
    def _build_admission_rule(cls, attributes: dict, rule_type: GcpBinaryAuthorizationAdmissionRuleType, cluster_id: Optional[str] = None):
        return GcpBinaryAuthorizationAdmissionRule(admission_rule_type=rule_type,
                                                   evaluation_mode=enum_implementation(GcpBinaryAuthorizationAdmissionEvaluationMode,
                                                                                       cls._get_known_value(attributes, 'evaluation_mode')),
                                                   enforcement_mode=enum_implementation(GcpBinaryAuthorizationAdmissionEnforcementMode,
                                                                                       cls._get_known_value(attributes, 'enforcement_mode')),
                                                   cluster_id=cluster_id)
