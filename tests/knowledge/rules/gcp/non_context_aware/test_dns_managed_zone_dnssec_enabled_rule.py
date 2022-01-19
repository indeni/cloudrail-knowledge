from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import GcpDnsManagedZone, GcpDnsManagedZoneDnsSecCfg
from cloudrail.knowledge.rules.gcp.non_context_aware.dns_managed_zone_dnssec_enabled_rule import DnsManagedZoneDnssecEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestDnsManagedZoneDnssecEnabledRule(TestCase):
    def setUp(self):
        self.rule = DnsManagedZoneDnssecEnabledRule()

    @parameterized.expand(
        [
            ["dnssec_enabled", 'on', 0, RuleResultType.SUCCESS],
            ["dnssec_disabled", 'off', 1, RuleResultType.FAILED],
        ]
    )

    def test_dns_managed_zone_dnssec_enabled(self, unused_name: str, dnssec_state: str, total_issues: int, rule_status: RuleResultType):
        # Arrange
        dns_managed_zone: GcpDnsManagedZone = create_empty_entity(GcpDnsManagedZone)
        dns_sec_config: GcpDnsManagedZoneDnsSecCfg = create_empty_entity(GcpDnsManagedZoneDnsSecCfg)
        dns_sec_config.state = dnssec_state
        dns_managed_zone.dnssec_config = dns_sec_config

        context = GcpEnvironmentContext(dns_managed_zones=[dns_managed_zone])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
