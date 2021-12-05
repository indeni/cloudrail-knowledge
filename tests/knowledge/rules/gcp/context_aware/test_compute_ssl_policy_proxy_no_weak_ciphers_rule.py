from typing import List
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_https_proxy import GcpComputeTargetHttpsProxy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_ssl_proxy import GcpComputeTargetSslProxy
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.context_aware.compute_ssl_policy_proxy_no_weak_ciphers_rule import ComputeSslPolicyProxyNoWeakCiphersRule


class TestComputeSslPolicyProxyNoWeakCiphersRule(TestCase):
    def setUp(self):
        self.rule = ComputeSslPolicyProxyNoWeakCiphersRule()

    @parameterized.expand(
        [
            ["HTTPS strong policy", GcpComputeTargetHttpsProxy, "MODERN", "TLS_1_2", [], 0, RuleResultType.SUCCESS],
            ["HTTPS weak policy ciphers", GcpComputeTargetHttpsProxy, "CUSTOM", "TLS_1_2",
             ["TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"], 1, RuleResultType.FAILED],
            ["HTTPS weak policy tls", GcpComputeTargetHttpsProxy, "MODERN", "TLS_1_0", [], 1, RuleResultType.FAILED],
            ["SSL strong policy", GcpComputeTargetSslProxy,  "MODERN", "TLS_1_2", [], 0, RuleResultType.SUCCESS],
            ["SSL weak policy ciphers", GcpComputeTargetSslProxy, "CUSTOM", "TLS_1_2",
             ["TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"], 1, RuleResultType.FAILED],
            ["SSL weak policy tls", GcpComputeTargetSslProxy, "MODERN", "TLS_1_0", [], 1, RuleResultType.FAILED],
        ]
    )

    def test_global_forwarding_rule_no_weak_policy(self, unused_name: str, target_class: GcpComputeTargetProxy, profile: str, version: str, custom_features: List[str],
                                                   total_issues: int, rule_status: RuleResultType):
        # Arrange
        global_forwarding_rule: GcpComputeGlobalForwardingRule = create_empty_entity(GcpComputeGlobalForwardingRule)
        target_proxy = create_empty_entity(target_class)
        global_forwarding_rule.target = target_proxy
        ssl_policy = create_empty_entity(GcpComputeSslPolicy)
        global_forwarding_rule.target.ssl_policy = ssl_policy
        global_forwarding_rule.target.ssl_policy.profile = profile
        global_forwarding_rule.target.ssl_policy.min_tls_version = version
        global_forwarding_rule.target.ssl_policy.custom_features = custom_features

        context = GcpEnvironmentContext()
        if isinstance(target_proxy, GcpComputeTargetHttpsProxy):
            context = GcpEnvironmentContext(compute_global_forwarding_rule=[global_forwarding_rule],
                                            compute_target_https_proxy=AliasesDict(target_proxy),
                                            compute_ssl_policy=AliasesDict(ssl_policy))
        if isinstance(target_proxy, GcpComputeTargetSslProxy):
            context = GcpEnvironmentContext(compute_global_forwarding_rule=[global_forwarding_rule],
                                            compute_target_ssl_proxy=AliasesDict(target_proxy),
                                            compute_ssl_policy=AliasesDict(ssl_policy))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
