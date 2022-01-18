from typing import List, Optional
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpBinaryAuthorizationAdmissionEnforcementMode, \
    GcpBinaryAuthorizationAdmissionEvaluationMode, GcpBinaryAuthorizationAdmissionRule, GcpBinaryAuthorizationAdmissionRuleType, GcpClusterContainerBinaryAuthorizationPolicy
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.context_aware.container_cluster_use_authorization_policy_rule import ContainerClusterUseAuthorizationPolicyRule


class TestContainerClusterUseAuthorizationPolicyRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterUseAuthorizationPolicyRule()

    @parameterized.expand(
        [
            ["no_auth_policy_used", False, None, None, 1, RuleResultType.FAILED],
            ["auth_policy_enabled_default_allow", True, GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_ALLOW,
             GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_DENY, 1, RuleResultType.FAILED],
            ["auth_policy_enabled_default_deny_cluster_allow", True, GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_DENY,
             GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_ALLOW, 1, RuleResultType.FAILED],
            ["auth_policy_enabled_both_admission_deny", True, GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_DENY,
             GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_DENY, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_use_binary_auth_policy(self, unused_name: str,
                                                      enable_binary_authorization: bool,
                                                      default_admission_evaluation_mode: Optional[GcpBinaryAuthorizationAdmissionEvaluationMode],
                                                      cluster_admission_evaluation_mode: Optional[GcpBinaryAuthorizationAdmissionEvaluationMode],
                                                      total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster: GcpContainerCluster = create_empty_entity(GcpContainerCluster)
        container_cluster.enable_binary_authorization = enable_binary_authorization
        binary_auth_policy: GcpClusterContainerBinaryAuthorizationPolicy = create_empty_entity(GcpClusterContainerBinaryAuthorizationPolicy)
        binary_auth_policy.default_admission_rule = GcpBinaryAuthorizationAdmissionRule(GcpBinaryAuthorizationAdmissionRuleType.DEFAULT,
                                                                                        default_admission_evaluation_mode,
                                                                                        GcpBinaryAuthorizationAdmissionEnforcementMode.ENFORCED_BLOCK_AND_AUDIT_LOG,
                                                                                        None)
        cluster_admission_rules: List[GcpBinaryAuthorizationAdmissionRule] = []
        binary_auth_policy.cluster_admission_rules = cluster_admission_rules
        binary_auth_policy.cluster_admission_rules.append(GcpBinaryAuthorizationAdmissionRule(GcpBinaryAuthorizationAdmissionRuleType.CLUSTER,
                                                                                              cluster_admission_evaluation_mode,
                                                                                              GcpBinaryAuthorizationAdmissionEnforcementMode.ENFORCED_BLOCK_AND_AUDIT_LOG, 'cluster_id'))
        container_cluster.binary_auth_policies = [binary_auth_policy.default_admission_rule, binary_auth_policy.cluster_admission_rules[0]]
        context = GcpEnvironmentContext(container_cluster=[container_cluster],
                                        binary_authorization_policies=[binary_auth_policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
