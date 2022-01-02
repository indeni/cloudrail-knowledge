from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.compute_ssl_policy_proxy_no_weak_ciphers_rule import ComputeSslPolicyProxyNoWeakCiphersRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeSslPolicyProxyNoWeakCiphersRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeSslPolicyProxyNoWeakCiphersRule()

    @rule_test('global_forwarding_rule_with_https_proxy_and_strong_policy', should_alert=False)
    def test_with_https_proxy_and_strong_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('global_forwarding_rule_with_https_proxy_and_weak_policy_ciphers', should_alert=True)
    def test_with_https_proxy_and_weak_policy_ciphers(self, rule_result: RuleResponse):
        pass

    @rule_test('global_forwarding_rule_with_https_proxy_and_weak_policy_tls', should_alert=True)
    def test_with_https_proxy_and_weak_policy_tls(self, rule_result: RuleResponse):
        pass

    @rule_test('global_forwarding_rule_with_ssl_proxy_and_strong_policy', should_alert=False)
    def test_with_ssl_proxy_and_strong_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('global_forwarding_rule_with_ssl_proxy_and_weak_policy_ciphers', should_alert=True)
    def test_with_ssl_proxy_and_weak_policy_ciphers(self, rule_result: RuleResponse):
        pass

    @rule_test('global_forwarding_rule_with_ssl_proxy_and_weak_policy_tls', should_alert=True)
    def test_with_ssl_proxy_and_weak_policy_tls(self, rule_result: RuleResponse):
        pass
