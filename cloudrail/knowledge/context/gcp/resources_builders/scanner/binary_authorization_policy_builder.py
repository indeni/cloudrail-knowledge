from typing import Optional, List
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpClusterContainerBinaryAuthorizationPolicy, \
    GcpBinaryAuthorizationAdmissionRuleType, GcpBinaryAuthorizationAdmissionRule, GcpBinaryAuthorizationAdmissionEvaluationMode, \
    GcpBinaryAuthorizationAdmissionEnforcementMode
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation

class BinaryAuthorizationPolicyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'binaryauthorization-v1-projects-getPolicy.json'

    def do_build(self, attributes: dict) -> GcpClusterContainerBinaryAuthorizationPolicy:
        cluster_admission_rules: List[GcpBinaryAuthorizationAdmissionRule] = []
        for rule in attributes.get('clusterAdmissionRules', {}):
            cluster_admission_rules.append(self._build_admission_rule(attributes['clusterAdmissionRules'][rule], GcpBinaryAuthorizationAdmissionRuleType.CLUSTER, rule))
        global_policy_evaluation_mode_enabled = attributes.get('globalPolicyEvaluationMode') == 'ENABLE'
        return GcpClusterContainerBinaryAuthorizationPolicy(default_admission_rule=self._build_admission_rule(attributes['defaultAdmissionRule'],
                                                                                                              GcpBinaryAuthorizationAdmissionRuleType.DEFAULT),
                                                            cluster_admission_rules=cluster_admission_rules,
                                                            global_policy_evaluation_mode_enabled=global_policy_evaluation_mode_enabled)

    @classmethod
    def _build_admission_rule(cls, attributes: dict, rule_type: GcpBinaryAuthorizationAdmissionRuleType, cluster_id: Optional[str] = None):
        return GcpBinaryAuthorizationAdmissionRule(admission_rule_type=rule_type,
                                                   evaluation_mode=enum_implementation(GcpBinaryAuthorizationAdmissionEvaluationMode, attributes['evaluationMode']),
                                                   enforcement_mode=enum_implementation(GcpBinaryAuthorizationAdmissionEnforcementMode, attributes['enforcementMode']),
                                                   cluster_id=cluster_id)
