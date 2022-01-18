from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpBinaryAuthorizationAdmissionRule, \
    GcpBinaryAuthorizationAdmissionRuleType, GcpBinaryAuthorizationAdmissionEvaluationMode, GcpBinaryAuthorizationAdmissionEnforcementMode

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestBinaryAuthorizationPolicy(GcpContextTest):
    def get_component(self):
        return 'binary_authorization_policy'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        policy = next((policy for policy in ctx.binary_authorization_policies if policy.project_id == 'dev-for-tests'), None)
        self.assertIsNotNone(policy)
        self.assertFalse(policy.global_policy_evaluation_mode_enabled)
        self.assertEqual(policy.default_admission_rule,
                         GcpBinaryAuthorizationAdmissionRule(GcpBinaryAuthorizationAdmissionRuleType.DEFAULT,
                                                             GcpBinaryAuthorizationAdmissionEvaluationMode.ALWAYS_DENY,
                                                             GcpBinaryAuthorizationAdmissionEnforcementMode.ENFORCED_BLOCK_AND_AUDIT_LOG,
                                                             None))
        self.assertTrue(len(policy.cluster_admission_rules), 1)
        self.assertEqual(policy.cluster_admission_rules[0],
                         GcpBinaryAuthorizationAdmissionRule(GcpBinaryAuthorizationAdmissionRuleType.CLUSTER,
                                                             GcpBinaryAuthorizationAdmissionEvaluationMode.REQUIRE_ATTESTATION,
                                                             GcpBinaryAuthorizationAdmissionEnforcementMode.ENFORCED_BLOCK_AND_AUDIT_LOG,
                                                             'us-west1-a.gke-cluster-007'))
        container_cluster = next((cluster for cluster in ctx.container_clusters if cluster.name == 'gke-cluster-007'), None)
        self.assertIsNotNone(container_cluster)
        self.assertTrue(len(container_cluster.binary_auth_policies), 2)
        self.assertTrue(any(policy.enforcement_mode == GcpBinaryAuthorizationAdmissionEnforcementMode.ENFORCED_BLOCK_AND_AUDIT_LOG
                            for policy in container_cluster.binary_auth_policies))
