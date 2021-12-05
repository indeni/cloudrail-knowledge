from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import GcpDnsManagedZone, GcpDnsManagedZoneDnsSecCfg, GcpDnsManagedZoneDnsSecCfgDefKeySpecs, DnsDefKeyAlgorithm
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.cloud_dns_no_rsasha1_used_rules import CloudDnsNoRsasha1UsedRule


class TestCloudDnsNoRsasha1UsedRule(TestCase):
    def setUp(self):
        self.rule = CloudDnsNoRsasha1UsedRule()

    @parameterized.expand(
        [
            ["rsasha1_used", 'rsasha1', True],
            ["rsasha1_used", 'rsasha256', False],
        ]
    )

    def test_cloud_dns_rsasha1_usage(self, unused_name: str, rsa_version: str, should_alert: bool):
        # Arrange
        dns_managed_zone = create_empty_entity(GcpDnsManagedZone)
        dns_config = create_empty_entity(GcpDnsManagedZoneDnsSecCfg)
        default_key_conf = create_empty_entity(GcpDnsManagedZoneDnsSecCfgDefKeySpecs)
        default_key_conf.algorithm = DnsDefKeyAlgorithm(rsa_version)
        dns_config.default_key_specs = [default_key_conf]
        dns_config.state = 'on'
        dns_managed_zone.dnssec_config = dns_config
        context = GcpEnvironmentContext(dns_managed_zones=[dns_managed_zone])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
