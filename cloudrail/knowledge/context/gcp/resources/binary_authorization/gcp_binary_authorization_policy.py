import dataclasses
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpBinaryAuthorizationAdmissionRuleType(str, Enum):
    DEFAULT = 'default'
    CLUSTER = 'cluster'


class GcpBinaryAuthorizationAdmissionEvaluationMode(str, Enum):
    EVALUATION_MODE_UNSPECIFIED = None
    ALWAYS_ALLOW = 'ALWAYS_ALLOW'
    REQUIRE_ATTESTATION = 'REQUIRE_ATTESTATION'
    ALWAYS_DENY = 'ALWAYS_DENY'


class GcpBinaryAuthorizationAdmissionEnforcementMode(str, Enum):
    ENFORCEMENT_MODE_UNSPECIFIED = None
    ENFORCED_BLOCK_AND_AUDIT_LOG = 'ENFORCED_BLOCK_AND_AUDIT_LOG'
    DRYRUN_AUDIT_LOG_ONLY = 'DRYRUN_AUDIT_LOG_ONLY'


@dataclass
class GcpBinaryAuthorizationAdmissionRule:
    """
        Attributes:
            admission_rule_type: The admission rule type: either the default or cluster.
	        evaluation_mode: (Required) Evaluation mode for container image authorization. Possible values are ALWAYS_ALLOW, REQUIRE_ATTESTATION, and ALWAYS_DENY.
	        enforcement_mode: (Required) Action when a pod creation is denied by the admission rule. Possible values are ENFORCED_BLOCK_AND_AUDIT_LOG and DRYRUN_AUDIT_LOG_ONLY.
            cluster_id: (Optional) The identifier for this object, in a format of loaction.cluster name. If this object rule is specific to a cluster.
    """
    admission_rule_type: GcpBinaryAuthorizationAdmissionRuleType
    evaluation_mode: GcpBinaryAuthorizationAdmissionEvaluationMode
    enforcement_mode: GcpBinaryAuthorizationAdmissionEnforcementMode
    cluster_id: Optional[str]


class GcpClusterContainerBinaryAuthorizationPolicy(GcpResource):
    """
        Attributes:
            default_admission_rule: (Required) Default admission rule for a cluster without a per-cluster admission rule.
            cluster_admission_rules: (Optional) List of per-cluster admission rules.
            global_policy_evaluation_mode_enabled: (Optional) Indication if the evaluation of a Google-maintained global admission policy for common system-level images is enabled.
    """

    def __init__(self,
                 default_admission_rule: GcpBinaryAuthorizationAdmissionRule,
                 cluster_admission_rules: List[GcpBinaryAuthorizationAdmissionRule],
                 global_policy_evaluation_mode_enabled: bool):

        super().__init__(GcpResourceType.GOOGLE_BINARY_AUTHORIZATION_POLICY)
        self.default_admission_rule: GcpBinaryAuthorizationAdmissionRule = default_admission_rule
        self.cluster_admission_rules: List[GcpBinaryAuthorizationAdmissionRule] = cluster_admission_rules
        self.global_policy_evaluation_mode_enabled: bool = global_policy_evaluation_mode_enabled

    def get_keys(self) -> List[str]:
        return [self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}security/binary-authorization/policy?referrer=search&project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Cluster Binary Authorization Policy Detail'
        else:
            return 'Cluster Binary Authorization Policy Details'

    def to_drift_detection_object(self) -> dict:
        return {'default_admission_rule': self.default_admission_rule and dataclasses.asdict(self.default_admission_rule),
                'cluster_admission_rules': self.cluster_admission_rules and [dataclasses.asdict(rule) for rule in self.cluster_admission_rules],
                'global_policy_evaluation_mode_enabled': self.global_policy_evaluation_mode_enabled}
