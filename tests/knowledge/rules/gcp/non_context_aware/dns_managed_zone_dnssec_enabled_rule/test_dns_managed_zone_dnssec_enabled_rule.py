from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.dns_managed_zone_dnssec_enabled_rule import DnsManagedZoneDnssecEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestDnsManagedZoneDnssecEnabledRule(GcpBaseRuleTest):

    def get_rule(self):
        return DnsManagedZoneDnssecEnabledRule()

    @rule_test('dnssec_disabled', should_alert=True)
    def test_dnssec_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('dnssec_enabled', should_alert=False)
    def test_dnssec_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('private_zone_dnssec_disabled', should_alert=True)
    def test_private_zone_dnssec_disabled(self, rule_result: RuleResponse):
        pass
