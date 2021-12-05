from typing import List
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import GcpDnsManagedZone, GcpDnsManagedZoneDnsSecCfg, GcpDnsManagedZoneDnsSecCfgDefKeySpecs, DnsDefKeyAlgorithm, DnsDefKeyType
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class GcpDnsManagedZoneBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'dns-v1beta2-managedZones-list.json'

    def do_build(self, attributes: dict) -> GcpDnsManagedZone:
        ## DNS security config
        dnssec_config = None
        if dnssec_config_data := attributes.get('dnssecConfig'):
            ## Default Key Specs config
            default_key_specs: List[GcpDnsManagedZoneDnsSecCfgDefKeySpecs] = []
            for default_key_specs_data in dnssec_config_data.get('defaultKeySpecs', []):
                default_key_specs.append(GcpDnsManagedZoneDnsSecCfgDefKeySpecs(algorithm=DnsDefKeyAlgorithm(default_key_specs_data.get('algorithm', 'None')),
                                                                               key_length=default_key_specs_data['keyLength'],
                                                                               key_type=DnsDefKeyType(default_key_specs_data['keyType']),
                                                                               kind=default_key_specs_data['kind']))
            dnssec_config = GcpDnsManagedZoneDnsSecCfg(kind=dnssec_config_data['kind'],
                                                       non_existence=dnssec_config_data['nonExistence'],
                                                       state=dnssec_config_data['state'],
                                                       default_key_specs=default_key_specs)
        return GcpDnsManagedZone(name=attributes['name'],
                                 dns_name=attributes['dnsName'],
                                 description=attributes.get('description'),
                                 dnssec_config=dnssec_config)
