from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import DnsDefKeyAlgorithm, DnsDefKeyType

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestGcpDnsManagedZone(GcpContextTest):
    def get_component(self):
        return 'dns_managed_zone'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        dns = next((dns for dns in ctx.dns_managed_zones if dns.name == 'test-zone'), None)
        self.assertIsNotNone(dns)
        self.assertEqual(dns.description, 'Example DNS managed zone for cloudrail')
        self.assertEqual(dns.dns_name, 'testing.example.com.')
        self.assertTrue(dns.dnssec_config)
        self.assertEqual(dns.dnssec_config.kind, 'dns#managedZoneDnsSecConfig')
        self.assertEqual(dns.dnssec_config.non_existence, 'nsec3')
        self.assertEqual(dns.dnssec_config.state, 'on')
        self.assertEqual(len(dns.dnssec_config.default_key_specs), 2)
        for default_key in dns.dnssec_config.default_key_specs:
            self.assertEqual(default_key.kind, 'dns#dnsKeySpec')
            self.assertEqual(default_key.key_length, 2048)
        zone_sign_key = next((key for key in dns.dnssec_config.default_key_specs if key.key_type == DnsDefKeyType.ZONESIGNING), None)
        self.assertEqual(zone_sign_key.algorithm, DnsDefKeyAlgorithm.RSASHA256)
        key_sign_type = next((key for key in dns.dnssec_config.default_key_specs if key.key_type == DnsDefKeyType.KEYSIGNING), None)
        self.assertEqual(key_sign_type.algorithm, DnsDefKeyAlgorithm.RSASHA512)
